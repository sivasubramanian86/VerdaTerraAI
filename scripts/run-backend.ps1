Param()
Write-Host "Starting backend services..."

# Optional: remind about installing dependencies
if (Test-Path requirements.txt) { Write-Host "(Tip) install Python deps: pip install -r requirements.txt" }

$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $projectRoot

# Set PYTHONPATH so verdaterrakai package can be imported
$env:PYTHONPATH = Join-Path $projectRoot "..\verdaterrakai\src"

Write-Host "Starting ingress API on http://localhost:8080"
$ingressArgs = @(
	'-m', 'uvicorn', 'backend.app.main:app',
	'--reload', '--host', '0.0.0.0', '--port', '8080'
)
Start-Process -NoNewWindow -FilePath python -ArgumentList $ingressArgs -WorkingDirectory $projectRoot

Write-Host "Starting agent API on http://localhost:8081"
$agentArgs = @(
	'-m', 'uvicorn', 'verdaterrakai.app.main:app',
	'--reload', '--host', '0.0.0.0', '--port', '8081'
)
Start-Process -NoNewWindow -FilePath python -ArgumentList $agentArgs -WorkingDirectory $projectRoot

Write-Host "Started backend processes. Check their terminals or logs."
