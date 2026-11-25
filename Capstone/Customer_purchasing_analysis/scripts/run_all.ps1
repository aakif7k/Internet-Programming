# scripts/run_all.ps1: Starts R Analytics, FastAPI Backend, and React Frontend in separate windows and opens browser
$ErrorActionPreference = "Stop"

$Root = Split-Path -Parent $PSScriptRoot
$SessionDir = if ($env:SESSION_DIR) { $env:SESSION_DIR } else { Join-Path $Root "temp_sessions" }
if (!(Test-Path $SessionDir)) {
    New-Item -ItemType Directory -Force -Path $SessionDir | Out-Null
}

Write-Host "=================================================================" -ForegroundColor Cyan
Write-Host " Launching Clickstream Analytics & Revenue Capstone Web App" -ForegroundColor Cyan
Write-Host " 1. R Analytics Service (:8001)"
Write-Host " 2. Python FastAPI Backend (:8000)"
Write-Host " 3. React Vite UI (:5173)"
Write-Host "=================================================================" -ForegroundColor Cyan

# Start R Analytics
Start-Process powershell -ArgumentList "-NoExit", "-ExecutionPolicy", "Bypass", "-File", "`"$PSScriptRoot\run_r_analytics.ps1`""
Write-Host "[1/3] R Analytics started on port 8001" -ForegroundColor Green
Start-Sleep -Seconds 3

# Start FastAPI Backend
Start-Process powershell -ArgumentList "-NoExit", "-ExecutionPolicy", "Bypass", "-File", "`"$PSScriptRoot\run_backend.ps1`""
Write-Host "[2/3] FastAPI Backend started on port 8000" -ForegroundColor Green
Start-Sleep -Seconds 2

# Start Frontend
Start-Process powershell -ArgumentList "-NoExit", "-ExecutionPolicy", "Bypass", "-File", "`"$PSScriptRoot\run_frontend.ps1`""
Write-Host "[3/3] Frontend started on port 5173" -ForegroundColor Green
Start-Sleep -Seconds 3

# Open Browser
Write-Host "Opening web application in default browser: http://localhost:5173" -ForegroundColor Yellow
Start-Process "http://localhost:5173"
