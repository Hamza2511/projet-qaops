"""Scan actif ZAP exclusivement sur le démonstrateur local fourni."""
import argparse
import importlib.util
import json
from pathlib import Path
import subprocess
import threading
from datetime import datetime, timezone

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--zap-jar', type=Path, required=True)
parser.add_argument('--work-dir', type=Path, required=True)
args = parser.parse_args()
root = Path(__file__).resolve().parents[1]
out = root / 'reports/security-local'
out.mkdir(parents=True, exist_ok=True)
work = args.work_dir.resolve()
work.mkdir(parents=True, exist_ok=True)
spec = importlib.util.spec_from_file_location('xss_lab', root/'security/xss_lab.py')
lab = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lab)
server = lab.ThreadingHTTPServer(('127.0.0.1', 18094), lab.Handler)
thread = threading.Thread(target=server.serve_forever, daemon=True)
thread.start()
plan = {
 'env': {'contexts': [{'name': 'QAOpsLocal', 'urls': ['http://127.0.0.1:18094'],
                      'includePaths': ['http://127\\.0\\.0\\.1:18094/(vulnerable|fixed).*']}],
         'parameters': {'failOnError': True, 'failOnWarning': False, 'progressToStdout': True}},
 'jobs': [
   {'type': 'requestor', 'requests': [{'url': f'http://127.0.0.1:18094/{route}?q=Sara', 'method': 'GET', 'responseCode': 200} for route in ['vulnerable', 'fixed']]},
   {'type': 'activeScan', 'parameters': {'context': 'QAOpsLocal', 'maxRuleDurationInMins': 1, 'maxScanDurationInMins': 2, 'threadPerHost': 1, 'delayInMs': 20},
    'policyDefinition': {'defaultStrength': 'Medium', 'defaultThreshold': 'Off', 'rules': [{'id': 40012, 'strength': 'Medium', 'threshold': 'Medium'}]}},
   {'type': 'passiveScan-wait', 'parameters': {'maxDuration': 1}},
   *[{'type': 'report', 'parameters': {'template': 'traditional-'+fmt, 'reportDir': str(out), 'reportFile': 'zap-local.'+fmt, 'reportTitle': 'QAOps - XSS local avant et après correction'}} for fmt in ['json','html']],
 ]}
config = work/'xss-local.yaml'
config.write_text(json.dumps(plan, ensure_ascii=False, indent=2), encoding='utf-8')
(out/'scan-plan.json').write_text(json.dumps(plan, ensure_ascii=False, indent=2), encoding='utf-8')
try:
    with (out/'execution.log').open('w', encoding='utf-8') as log:
        result = subprocess.run(['java','-Xmx512m','-jar',str(args.zap_jar.resolve()),'-cmd','-port','18092','-dir',str(work/'zap-home'),'-autorun',str(config)], stdout=log, stderr=subprocess.STDOUT, timeout=300)
    report = json.loads((out/'zap-local.json').read_text(encoding='utf-8'))
    alerts = [a for site in report.get('site',[]) for a in site.get('alerts',[]) if str(a.get('pluginid')) == '40012']
    urls = sorted({i['uri'] for a in alerts for i in a.get('instances',[])})
    assert result.returncode == 0, f'ZAP returned {result.returncode}'
    assert any('/vulnerable?' in url for url in urls), 'Expected XSS not detected on vulnerable fixture'
    assert not any('/fixed?' in url for url in urls), 'XSS detected after correction'
    summary = {'recorded_at_utc': datetime.now(timezone.utc).isoformat(), 'target': 'loopback-only educational fixture', 'zap_exit_code': result.returncode, 'xss_rule': 40012, 'vulnerable_detected': True, 'fixed_xss_detected': False, 'xss_urls': urls, 'limitation': 'This controlled example does not demonstrate an exploitable XSS on Formy.'}
    (out/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(summary,ensure_ascii=False))
finally:
    server.shutdown()
    server.server_close()
