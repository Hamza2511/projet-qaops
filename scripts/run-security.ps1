$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path $PSScriptRoot -Parent
$reportDir = Join-Path $projectRoot 'reports/security'
New-Item -ItemType Directory -Force -Path $reportDir | Out-Null
Copy-Item -LiteralPath (Join-Path $projectRoot 'security/baseline.conf') -Destination $reportDir
docker run --rm -v "${reportDir}:/zap/wrk/:rw" ghcr.io/zaproxy/zaproxy:stable zap-baseline.py -t https://formy-project.herokuapp.com -m 1 -T 5 -c baseline.conf -r zap.html -J zap.json -w zap.md
$scanCode = $LASTEXITCODE
@{exit_code=$scanCode;date=(Get-Date -Format o);target='https://formy-project.herokuapp.com'} | ConvertTo-Json | Set-Content -Encoding utf8 (Join-Path $reportDir 'status.json')
exit $scanCode
