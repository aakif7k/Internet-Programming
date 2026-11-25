# scripts/run_frontend.ps1: Starts React Vite Frontend on port 5173
$ErrorActionPreference = "Stop"

$Root = Split-Path -Parent $PSScriptRoot

Write-Host "=================================================" -ForegroundColor Magenta
Write-Host " Starting React + TypeScript Frontend on :5173" -ForegroundColor Magenta
Write-Host " URL: http://localhost:5173"
Write-Host "=================================================" -ForegroundColor Magenta

Set-Location (Join-Path $Root "frontend")
npm run dev -- --host
