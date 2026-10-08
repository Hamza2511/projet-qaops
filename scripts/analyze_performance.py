"""Analyse un JTL CSV réel ; les seuils sont des objectifs pédagogiques, pas un SLA Reqres."""
import csv, json, math, sys
from pathlib import Path
rows=list(csv.DictReader(Path(sys.argv[1]).open(encoding='utf-8-sig')))
if not rows: raise SystemExit('JTL vide : aucun résultat exploitable')
def metrics(data):
    times=sorted(float(r['elapsed']) for r in data)
    start=min(float(r['timeStamp']) for r in data)
    end=max(float(r['timeStamp'])+float(r['elapsed']) for r in data)
    errors=sum(r['success'].lower()!='true' for r in data)
    return {'requests':len(data),'mean_ms':round(sum(times)/len(times),2),'p95_ms':times[math.ceil(.95*len(times))-1], 'throughput_rps':round(len(data)/max((end-start)/1000,.001),2), 'error_rate_pct':round(errors/len(data)*100,2)}
result={'overall':metrics(rows),'by_label':{name:metrics([r for r in rows if r['label']==name]) for name in sorted({r['label'] for r in rows})}}
result['passed']=result['overall']['p95_ms']<2000 and result['overall']['error_rate_pct']<1
Path(sys.argv[2]).write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps(result,indent=2))
raise SystemExit(0 if result['passed'] else 1)
