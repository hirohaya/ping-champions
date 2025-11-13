# Script para iniciar ngrok com múltiplos tunnels
# Expõe Backend (porta 8000) e Frontend (porta 5173)

Write-Host "==================================" -ForegroundColor Cyan
Write-Host "Iniciando ngrok Tunnels" -ForegroundColor Cyan
Write-Host "==================================" -ForegroundColor Cyan
Write-Host ""

# Cores para output
$successColor = "Green"
$infoColor = "Yellow"

Write-Host "Informações dos Servidores Locais:" -ForegroundColor $infoColor
Write-Host "  Backend: http://127.0.0.1:8000" -ForegroundColor White
Write-Host "  Frontend: http://localhost:5173" -ForegroundColor White
Write-Host ""

Write-Host "Iniciando ngrok..." -ForegroundColor $infoColor
Write-Host ""

# Opção 1: Subir apenas Backend (porta 8000)
Write-Host "Opção 1: Apenas Backend" -ForegroundColor Cyan
Write-Host "Comando: ngrok http 8000" -ForegroundColor Gray
Write-Host ""

# Opção 2: Subir ambos em terminais separados
Write-Host "Opção 2: Backend + Frontend (em terminais separados)" -ForegroundColor Cyan
Write-Host ""
Write-Host "Terminal 1 - Backend:" -ForegroundColor Yellow
Write-Host "  ngrok http 8000 --subdomain=pingchampions-api" -ForegroundColor Gray
Write-Host ""
Write-Host "Terminal 2 - Frontend:" -ForegroundColor Yellow
Write-Host "  ngrok http 5173 --subdomain=pingchampions-app" -ForegroundColor Gray
Write-Host ""

Write-Host "==================================" -ForegroundColor Cyan
Write-Host "Escolha uma opção (1 ou 2):" -ForegroundColor Cyan
Write-Host "==================================" -ForegroundColor Cyan
$choice = Read-Host "Digite 1 ou 2"

if ($choice -eq "1") {
    Write-Host ""
    Write-Host "Subindo ngrok para Backend (porta 8000)..." -ForegroundColor $successColor
    Write-Host "Sua URL pública será exibida abaixo" -ForegroundColor $infoColor
    Write-Host ""
    ngrok http 8000
} elseif ($choice -eq "2") {
    Write-Host ""
    Write-Host "Para ambos os servidores, abra 2 terminais diferentes e execute:" -ForegroundColor $infoColor
    Write-Host ""
    Write-Host "Terminal 1:" -ForegroundColor Cyan
    Write-Host "  ngrok http 8000 --subdomain=pingchampions-api" -ForegroundColor White
    Write-Host ""
    Write-Host "Terminal 2:" -ForegroundColor Cyan
    Write-Host "  ngrok http 5173 --subdomain=pingchampions-app" -ForegroundColor White
    Write-Host ""
    Write-Host "Pressione Enter para abrir Terminal 1..." -ForegroundColor Yellow
    Read-Host
    
    # Abre novo terminal para Backend
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PSScriptRoot'; ngrok http 8000 --subdomain=pingchampions-api"
    
    Write-Host "Agora abra outro terminal e execute Terminal 2" -ForegroundColor Yellow
} else {
    Write-Host "Opção inválida" -ForegroundColor Red
}
