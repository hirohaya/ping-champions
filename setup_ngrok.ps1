# Script para configurar ngrok com o Ping Champions
# Execução: .\setup_ngrok.ps1

Write-Host "=================================" -ForegroundColor Cyan
Write-Host "🚀 Setup ngrok para Ping Champions" -ForegroundColor Cyan
Write-Host "=================================" -ForegroundColor Cyan

# Verificar se ngrok está instalado
try {
    $ngrokVersion = ngrok version 2>&1
    Write-Host "✅ ngrok encontrado: $ngrokVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ ngrok não está instalado ou não está no PATH" -ForegroundColor Red
    Write-Host "   Baixe em: https://ngrok.com/download" -ForegroundColor Yellow
    exit 1
}

# Pedir a URL do ngrok ao usuário
Write-Host ""
Write-Host "Você tem duas opções:" -ForegroundColor Cyan
Write-Host ""
Write-Host "1️⃣  Deixar o script detectar automaticamente (requer ngrok rodando)"
Write-Host "2️⃣  Digitar a URL manualmente"
Write-Host ""

$choice = Read-Host "Escolha (1 ou 2)"

$ngrokUrl = $null

if ($choice -eq "1") {
    Write-Host ""
    Write-Host "Detectando URL do ngrok..." -ForegroundColor Yellow
    
    try {
        $response = Invoke-WebRequest -Uri "http://127.0.0.1:4040/api/tunnels" -ErrorAction Stop
        $tunnels = $response.Content | ConvertFrom-Json
        
        foreach ($tunnel in $tunnels.tunnels) {
            if ($tunnel.proto -eq "https") {
                $ngrokUrl = $tunnel.public_url
                break
            }
        }
        
        if ($ngrokUrl) {
            Write-Host "✅ URL encontrada: $ngrokUrl" -ForegroundColor Green
        } else {
            Write-Host "❌ Nenhum tunnel HTTPS encontrado" -ForegroundColor Red
            Write-Host "   Certifique-se de que ngrok está rodando: ngrok http 8000" -ForegroundColor Yellow
            exit 1
        }
    } catch {
        Write-Host "❌ Erro ao conectar ao ngrok (porta 4040)" -ForegroundColor Red
        Write-Host "   Verifique se ngrok está rodando: ngrok http 8000" -ForegroundColor Yellow
        exit 1
    }
} elseif ($choice -eq "2") {
    Write-Host ""
    $ngrokUrl = Read-Host "Digite a URL do ngrok (ex: https://abc123def45.ngrok.io)"
    
    if (-not $ngrokUrl.StartsWith("https://")) {
        Write-Host "❌ URL deve começar com https://" -ForegroundColor Red
        exit 1
    }
    
    Write-Host "✅ URL configurada: $ngrokUrl" -ForegroundColor Green
} else {
    Write-Host "❌ Opção inválida" -ForegroundColor Red
    exit 1
}

# Atualizar .env.local
Write-Host ""
Write-Host "📝 Atualizando .env.local..." -ForegroundColor Yellow

$envFile = ".\frontend\.env.local"
if (Test-Path $envFile) {
    $content = Get-Content $envFile -Raw
    
    if ($content -match "VITE_API_BASE_URL=") {
        $content = $content -replace "VITE_API_BASE_URL=.*", "VITE_API_BASE_URL=$ngrokUrl"
    } else {
        $content += "`nVITE_API_BASE_URL=$ngrokUrl`n"
    }
    
    Set-Content $envFile $content
    Write-Host "✅ .env.local atualizado" -ForegroundColor Green
} else {
    Write-Host "⚠️  Arquivo .env.local não encontrado" -ForegroundColor Yellow
    Write-Host "   Criando novo arquivo..." -ForegroundColor Yellow
    
    $content = @"
# Frontend Configuration
VITE_API_BASE_URL=$ngrokUrl
VITE_DEBUG=true
"@
    
    Set-Content $envFile $content
    Write-Host "✅ .env.local criado" -ForegroundColor Green
}

# Atualizar main.py (CORS)
Write-Host ""
Write-Host "📝 Atualizando main.py (CORS)..." -ForegroundColor Yellow

$mainFile = ".\backend\main.py"
$content = Get-Content $mainFile -Raw

# Padrão para encontrar URLs ngrok antigas
$pattern = '"https://[a-zA-Z0-9\-]*\.ngrok[a-zA-Z0-9\-]*\.dev"'

if ($content -match $pattern) {
    $content = $content -replace $pattern, "`"$ngrokUrl`""
    Write-Host "✅ URL ngrok antiga substituída" -ForegroundColor Green
} else {
    # Adicionar após localhost:5174
    $content = $content -replace '("http://localhost:5174",)', "`$1`n        `"$ngrokUrl`","
    Write-Host "✅ URL ngrok adicionada à lista CORS" -ForegroundColor Green
}

Set-Content $mainFile $content

# Resumo
Write-Host ""
Write-Host "=================================" -ForegroundColor Green
Write-Host "✅ Configuração Concluída!" -ForegroundColor Green
Write-Host "=================================" -ForegroundColor Green
Write-Host ""
Write-Host "📋 Próximos passos:" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. Reiniciar o backend:"
Write-Host "   python run_backend.py"
Write-Host ""
Write-Host "2. Reiniciar o frontend (nova janela):"
Write-Host "   cd frontend"
Write-Host "   npm run dev"
Write-Host ""
Write-Host "3. Acessar a aplicação:"
Write-Host "   $ngrokUrl (frontend)"
Write-Host ""
Write-Host "4. Login com credenciais de teste:"
Write-Host "   Email: admin@pingchampions.com"
Write-Host "   Senha: admin123"
Write-Host ""
Write-Host "=================================" -ForegroundColor Cyan
