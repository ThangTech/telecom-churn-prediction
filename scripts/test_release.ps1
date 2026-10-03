$ErrorActionPreference = 'Stop'

$root = Split-Path -Parent $PSScriptRoot
Set-Location -LiteralPath $root

python scripts/verify_release.py
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

python -m unittest discover -s tests -v
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Push-Location -LiteralPath (Join-Path $root 'web')
try {
    npm run lint
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    npm run test
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    npm run build
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
}
finally {
    Pop-Location
}

Write-Output 'Release verification passed.'
