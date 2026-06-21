Param()
Write-Host "Starting frontend dev server..."
Set-Location (Join-Path (Split-Path -Parent $MyInvocation.MyCommand.Path) "..\verdaterra-ui")

if (-not (Test-Path node_modules)) {
  Write-Host "Installing npm dependencies..."
  npm install
}

Write-Host "Running: npm run dev -- --host 0.0.0.0 --port 5173"
npm run dev -- --host 0.0.0.0 --port 5173
