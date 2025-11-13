#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Script simplificado para inicializar Ping Champions
    
.DESCRIPTION
    Inicia Backend -> Frontend -> mostra instruções para ngrok
    
.USAGE
    .\init_project_simple.ps1
#>

# Cores
$info = "Cyan"
$ok = "Green"
$warn = "Yellow"
$err = "Red"

$root = "c:\Users\hiros\OneDrive\Documents\ping-champions"
$backend = $root
$frontend = "$root\frontend"

Clear-Host

Write-Host "╔════════════════════════════════════════════════════╗" -ForegroundColor $info
Write-Host "║   🚀 Ping Champions - Init with ngrok             ║" -ForegroundColor $info
Write-Host "╚════════════════════════════════════════════════════╝" -ForegroundColor $info

# 1️⃣ BACKEND
Write-Host ""
Write-Host "[1/3] Verificando Backend..." -ForegroundColor $info

$python = Get-Process python -ErrorAction SilentlyContinue
if ($python) {
    Write-Host "✅ Backend já rodando (PID: $($python.Id))" -ForegroundColor $ok
} else {
    Write-Host "Iniciando Backend (http://127.0.0.1:8000)..." -ForegroundColor $warn
    Push-Location $backend
    Start-Process python -ArgumentList "run_backend.py" -NoNewWindow
    Start-Sleep -Seconds 3
    Pop-Location
    Write-Host "✅ Backend iniciado" -ForegroundColor $ok
}

# 2️⃣ FRONTEND
Write-Host ""
Write-Host "[2/3] Verificando Frontend..." -ForegroundColor $info

$node = Get-Process node -ErrorAction SilentlyContinue
if ($node) {
    Write-Host "✅ Frontend já rodando (PID: $($node.Id))" -ForegroundColor $ok
} else {
    Write-Host "Iniciando Frontend (http://localhost:5173)..." -ForegroundColor $warn
    Push-Location $frontend
    Start-Process npm -ArgumentList "run", "dev" -NoNewWindow
    Start-Sleep -Seconds 5
    Pop-Location
    Write-Host "✅ Frontend iniciado" -ForegroundColor $ok
}

# 3️⃣ NGROK
Write-Host ""
Write-Host "[3/3] Iniciando ngrok..." -ForegroundColor $info
Write-Host ""

Write-Host "════════════════════════════════════════════════════" -ForegroundColor $info
Write-Host "OPÇÕES NGROK:" -ForegroundColor $info
Write-Host "════════════════════════════════════════════════════" -ForegroundColor $info
Write-Host ""

Write-Host "📌 OPÇÃO 1 - URL Personalizada (ngrok PRO):" -ForegroundColor $warn
Write-Host "   ngrok http --url=unserialised-sherie-convocational.ngrok-free.dev 5173" -ForegroundColor $ok
Write-Host ""

Write-Host "📌 OPÇÃO 2 - URL Aleatória (ngrok FREE - RECOMENDADO):" -ForegroundColor $warn
Write-Host "   ngrok http 5173" -ForegroundColor $ok
Write-Host ""

Write-Host "════════════════════════════════════════════════════" -ForegroundColor $info
Write-Host "Escolha qual deseja executar:" -ForegroundColor $info
Write-Host "════════════════════════════════════════════════════" -ForegroundColor $info
Write-Host ""

Write-Host "[1] URL Personalizada (PRO)" -ForegroundColor $warn
Write-Host "[2] URL Aleatória (GRÁTIS) ⭐" -ForegroundColor $ok
Write-Host ""

$choice = Read-Host "Digite 1 ou 2"

Write-Host ""

if ($choice -eq "1") {
    Write-Host "Iniciando ngrok com URL personalizada..." -ForegroundColor $warn
    ngrok http --url=unserialised-sherie-convocational.ngrok-free.dev 5173
} elseif ($choice -eq "2") {
    Write-Host "Iniciando ngrok com URL aleatória..." -ForegroundColor $warn
    Write-Host "(Sua URL pública será exibida abaixo)" -ForegroundColor $info
    Write-Host ""
    ngrok http 5173
} else {
    Write-Host "Opção inválida" -ForegroundColor $err
    exit 1
}
