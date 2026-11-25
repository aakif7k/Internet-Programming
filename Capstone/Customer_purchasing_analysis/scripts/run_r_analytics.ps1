# scripts/run_r_analytics.ps1: Starts R Plumber analytics engine on port 8001
$ErrorActionPreference = "Stop"

$Root = Split-Path -Parent $PSScriptRoot
$DetectedR = (Get-Item "C:\Program Files\R\R-*\bin\Rscript.exe" -ErrorAction SilentlyContinue | Sort-Object FullName -Descending | Select-Object -First 1).FullName
$Rscript = if ($env:RSCRIPT_PATH) { 
    $env:RSCRIPT_PATH 
} elseif ($DetectedR) { 
    $DetectedR 
} elseif (Get-Command Rscript -ErrorAction SilentlyContinue) { 
    (Get-Command Rscript).Source 
} else { 
    "C:\Program Files\R\R-4.5.0\bin\Rscript.exe" 
}
$SessionDir = if ($env:SESSION_DIR) { $env:SESSION_DIR } else { Join-Path $Root "temp_sessions" }
$LibDir = Join-Path $Root "r-library"

if (!(Test-Path $Rscript)) {
    Write-Error "Rscript executable not found at: $Rscript. Please set RSCRIPT_PATH environment variable."
}

if (!(Test-Path $SessionDir)) {
    New-Item -ItemType Directory -Force -Path $SessionDir | Out-Null
}

$env:SESSION_DIR = $SessionDir

Write-Host "=================================================" -ForegroundColor Cyan
Write-Host " Starting R Analytics Service (Plumber) on :8001" -ForegroundColor Cyan
Write-Host " Rscript:     $Rscript"
Write-Host " Session Dir: $SessionDir"
Write-Host " R Library:   $LibDir"
Write-Host "=================================================" -ForegroundColor Cyan

Set-Location (Join-Path $Root "r-analytics")
& "$Rscript" server.R
