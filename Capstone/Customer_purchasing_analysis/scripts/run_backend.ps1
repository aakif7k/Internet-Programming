# scripts/run_backend.ps1: Starts Python FastAPI Backend on port 8000
$ErrorActionPreference = "Stop"

$Root = Split-Path -Parent $PSScriptRoot
$VenvPython = Join-Path $Root "venv\Scripts\python.exe"
$PythonExe = if (Test-Path $VenvPython) { $VenvPython } else { "python" }

$SessionDir = if ($env:SESSION_DIR) { $env:SESSION_DIR } else { Join-Path $Root "temp_sessions" }
$env:SESSION_DIR = $SessionDir
$env:R_SERVICE_URL = if ($env:R_SERVICE_URL) { $env:R_SERVICE_URL } else { "http://127.0.0.1:8001" }

if (!(Test-Path $SessionDir)) {
    New-Item -ItemType Directory -Force -Path $SessionDir | Out-Null
}

Write-Host "=================================================" -ForegroundColor Green
Write-Host " Starting FastAPI Backend on :8000" -ForegroundColor Green
Write-Host " Python:      $PythonExe"
Write-Host " Session Dir: $SessionDir"
Write-Host " R Service:   $($env:R_SERVICE_URL)"
Write-Host "=================================================" -ForegroundColor Green

Set-Location (Join-Path $Root "backend")
& "$PythonExe" -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload
