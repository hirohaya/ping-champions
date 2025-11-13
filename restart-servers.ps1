# Script para reinicializar Backend e Frontend
# Uso: .\restart-servers.ps1

param(
    [ValidateSet("backend", "frontend", "both")]
    [string]$Target = "both"
)

$BackendPath = "C:\Users\hiros\OneDrive\Documents\ping-champions"
$FrontendPath = "C:\Users\hiros\OneDrive\Documents\ping-champions\frontend"

function Stop-Servers {
    Write-Host "Parando servidores..." -ForegroundColor Yellow
    
    $pythonProcesses = Get-Process python -ErrorAction SilentlyContinue
    if ($pythonProcesses) {
        Write-Host "Matando Python (Backend)..." -ForegroundColor Cyan
        $pythonProcesses | Stop-Process -Force
        Start-Sleep -Seconds 1
    }
    
    $nodeProcesses = Get-Process node -ErrorAction SilentlyContinue
    if ($nodeProcesses) {
        Write-Host "Matando Node (Frontend)..." -ForegroundColor Cyan
        $nodeProcesses | Stop-Process -Force
        Start-Sleep -Seconds 1
    }
    
    Write-Host "Servidores parados." -ForegroundColor Green
}

function Start-Backend {
    Write-Host "Iniciando Backend..." -ForegroundColor Yellow
    Push-Location $BackendPath
    
    Write-Host "Executando: python run_backend.py" -ForegroundColor Cyan
    Write-Host "Backend deve estar em http://127.0.0.1:8000" -ForegroundColor Green
    
    & python run_backend.py
}

function Start-Frontend {
    Write-Host "Iniciando Frontend..." -ForegroundColor Yellow
    Push-Location $FrontendPath
    
    Write-Host "Executando: npm run dev" -ForegroundColor Cyan
    Write-Host "Frontend deve estar em http://localhost:5173" -ForegroundColor Green
    
    & npm run dev
}

# Executar baseado no parâmetro
switch ($Target) {
    "backend" {
        Stop-Servers
        Start-Backend
    }
    "frontend" {
        Stop-Servers
        Start-Frontend
    }
    "both" {
        Stop-Servers
        
        Write-Host "`n" -ForegroundColor White
        Write-Host "IMPORTANTE: Para rodar ambos, abra 2 PowerShells:" -ForegroundColor Yellow
        Write-Host "1. Primeiro PowerShell:" -ForegroundColor Cyan
        Write-Host "   cd $BackendPath" -ForegroundColor White
        Write-Host "   python run_backend.py" -ForegroundColor White
        Write-Host ""
        Write-Host "2. Segundo PowerShell:" -ForegroundColor Cyan
        Write-Host "   cd $FrontendPath" -ForegroundColor White
        Write-Host "   npm run dev" -ForegroundColor White
        Write-Host "`n" -ForegroundColor White
    }
}

Pop-Location
