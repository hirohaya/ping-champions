#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Script para inicializar Ping Champions com ngrok
    
.DESCRIPTION
    Inicia na ordem: Backend -> Frontend -> ngrok
    
.USAGE
    .\init_project_with_ngrok.ps1
#>

# Cores para output
$infoColor = "Cyan"
$successColor = "Green"
$warningColor = "Yellow"
$errorColor = "Red"

# Variáveis
$projectRoot = "c:\Users\hiros\OneDrive\Documents\ping-champions"
$backendDir = "$projectRoot"
$frontendDir = "$projectRoot\frontend"
$ngrokUrl = "unserialised-sherie-convocational.ngrok-free.dev"
$frontendPort = 5173
$backendPort = 8000

function Write-Header {
    param([string]$message)
    Write-Host ""
    Write-Host "╔══════════════════════════════════════════════════════════╗" -ForegroundColor $infoColor
    Write-Host "║ $message" -ForegroundColor $infoColor
    Write-Host "╚══════════════════════════════════════════════════════════╝" -ForegroundColor $infoColor
}

function Write-Step {
    param([string]$message, [string]$number)
    Write-Host ""
    Write-Host "[$number] $message" -ForegroundColor $infoColor
}

function Write-Success {
    param([string]$message)
    Write-Host "✅ $message" -ForegroundColor $successColor
}

function Write-Warning {
    param([string]$message)
    Write-Host "⚠️  $message" -ForegroundColor $warningColor
}

function Write-Error {
    param([string]$message)
    Write-Host "❌ $message" -ForegroundColor $errorColor
}

function Check-Process {
    param([string]$processName, [string]$port)
    $process = Get-Process $processName -ErrorAction SilentlyContinue
    if ($process) {
        Write-Success "$processName está rodando (PID: $($process.Id), Porta: $port)"
        return $true
    }
    return $false
}

# ============================================
# INÍCIO DO SCRIPT
# ============================================

Clear-Host
Write-Header "🚀 PING CHAMPIONS - Inicialização com ngrok"

Write-Host ""
Write-Host "Configuração:" -ForegroundColor $infoColor
Write-Host "  📁 Projeto: $projectRoot"
Write-Host "  🔧 Backend: $backendDir (porta $backendPort)"
Write-Host "  🎨 Frontend: $frontendDir (porta $frontendPort)"
Write-Host "  🌐 ngrok URL: $ngrokUrl"

# ============================================
# PASSO 1: Iniciar Backend
# ============================================

Write-Step "Verificando Backend" "1"

if (Check-Process "python" $backendPort) {
    Write-Warning "Backend já está rodando. Pulando inicialização..."
} else {
    Write-Host "Iniciando Backend (FastAPI)..." -ForegroundColor $infoColor
    
    try {
        Push-Location $backendDir
        # Inicia em background
        $backendProcess = Start-Process python -ArgumentList "run_backend.py" -NoNewWindow -PassThru
        Write-Success "Backend iniciado (PID: $($backendProcess.Id))"
        Write-Host "Aguardando inicialização..." -ForegroundColor $warningColor
        Start-Sleep -Seconds 3
        Pop-Location
    } catch {
        Write-Error "Falha ao iniciar Backend: $_"
        exit 1
    }
}

# ============================================
# PASSO 2: Iniciar Frontend
# ============================================

Write-Step "Verificando Frontend" "2"

$nodeProcesses = Get-Process "node" -ErrorAction SilentlyContinue
if ($nodeProcesses) {
    Write-Warning "Frontend já está rodando. Pulando inicialização..."
} else {
    Write-Host "Iniciando Frontend (Vue 3 + Vite)..." -ForegroundColor $infoColor
    
    try {
        Push-Location $frontendDir
        # Inicia em background
        $frontendProcess = Start-Process npm -ArgumentList "run", "dev" -NoNewWindow -PassThru
        Write-Success "Frontend iniciado (PID: $($frontendProcess.Id))"
        Write-Host "Aguardando inicialização..." -ForegroundColor $warningColor
        Start-Sleep -Seconds 5
        Pop-Location
    } catch {
        Write-Error "Falha ao iniciar Frontend: $_"
        exit 1
    }
}

# ============================================
# PASSO 3: Verificar Servidores
# ============================================

Write-Step "Verificando servidores" "3"

$backendOk = Check-Process "python" $backendPort
$frontendOk = $null -ne (Get-Process "node" -ErrorAction SilentlyContinue)

if ($backendOk) {
    Write-Success "Backend disponível em http://127.0.0.1:$backendPort"
} else {
    Write-Error "Backend não está respondendo"
}

if ($frontendOk) {
    Write-Success "Frontend disponível em http://localhost:$frontendPort"
} else {
    Write-Error "Frontend não está respondendo"
}

if (-not ($backendOk -and $frontendOk)) {
    Write-Error "Nem todos os serviços estão rodando. Abortando ngrok."
    exit 1
}

# ============================================
# PASSO 4: Iniciar ngrok com URL específica
# ============================================

Write-Step "Iniciando ngrok com URL específica" "4"

Write-Host ""
Write-Host "Informações do ngrok:" -ForegroundColor $infoColor
Write-Host "  🌐 URL Personalizada: $ngrokUrl"
Write-Host "  🔌 Port Frontend: $frontendPort"
Write-Host "  🔗 Comando: ngrok http --url=$ngrokUrl $frontendPort"
Write-Host ""

Write-Host "Iniciando ngrok..." -ForegroundColor $warningColor
Write-Host ""

try {
    # Inicia ngrok com a URL personalizada
    & ngrok http --url=$ngrokUrl $frontendPort
} catch {
    Write-Error "Falha ao iniciar ngrok: $_"
    exit 1
}

# ============================================
# FIM
# ============================================

Write-Host ""
Write-Host "Se você vê o erro acima sobre 'url', significa que:" -ForegroundColor $warningColor
Write-Host "  • Você está usando ngrok grátis (não suporta --url)"
Write-Host "  • Você precisa de plano ngrok Pro"
Write-Host "  • Use este comando em vez disso:" -ForegroundColor $infoColor
Write-Host ""
Write-Host "    ngrok http $frontendPort" -ForegroundColor $successColor
Write-Host ""
