# 🔧 Guia de Troubleshooting - Login via ngrok

## ❌ Problema: "Email ou senha inválido" ao usar ngrok

### Checklist de Verificação

#### 1️⃣ Verificar se o Backend está respondendo

```powershell
# Testar se o endpoint de login funciona localmente
$response = Invoke-WebRequest -Uri "http://127.0.0.1:8000/users/login" `
  -Method POST `
  -Headers @{"Content-Type"="application/json"} `
  -Body '{"email":"admin@pingchampions.com","password":"admin123"}'

$response.StatusCode
# Esperado: 200
```

Se retornar erro, o backend não está rodando. Iniciar com:
```powershell
python run_backend.py
```

---

#### 2️⃣ Verificar se ngrok está rodando

```powershell
# Abrir em um navegador ou terminal
http://127.0.0.1:4040/api/tunnels
```

Procurar por algo como:
```json
{
  "tunnels": [
    {
      "name": "command_line",
      "uri": "/tunnels/command_line",
      "public_url": "https://abc123def45.ngrok.io",
      "proto": "https",
      "config": {...},
      "metrics": {...}
    }
  ]
}
```

Se ngrok não estiver rodando:
```powershell
ngrok http 8000
```

---

#### 3️⃣ Verificar URL no Frontend (.env.local)

Abrir arquivo: `frontend/.env.local`

Verificar linha:
```bash
VITE_API_BASE_URL=https://YOUR_NGROK_URL.ngrok.io
```

Se estiver errada, atualizar com a URL correta do ngrok.

---

#### 4️⃣ Verificar CORS no Backend (main.py)

Abrir arquivo: `backend/main.py`

Procurar pela seção:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
        "https://YOUR_NGROK_URL.ngrok.io",  # ← Verificar se está aqui
    ],
    ...
)
```

Se a URL do ngrok não estiver na lista, adicionar.

---

#### 5️⃣ Testar Conexão CORS via curl

```powershell
# Testar via ngrok
$response = Invoke-WebRequest -Uri "https://YOUR_NGROK_URL.ngrok.io/users/login" `
  -Method POST `
  -Headers @{"Content-Type"="application/json"} `
  -Body '{"email":"admin@pingchampions.com","password":"admin123"}'

$response.StatusCode
# Esperado: 200
```

Se retornar erro 403 (Forbidden) ou erro de CORS, verificar allow_origins em main.py.

---

#### 6️⃣ Abrir DevTools no Navegador (F12)

1. Abrir o navegador com a URL do ngrok
2. Pressionar **F12** ou **Ctrl+Shift+I**
3. Ir na aba **Network**
4. Clicar em **Console** para ver mensagens
5. Tentar fazer login
6. Procurar pela requisição POST `/users/login` na aba Network
7. Verificar:
   - **URL**: Deve ser `https://YOUR_NGROK_URL.ngrok.io/users/login`
   - **Status**: Deve ser 200
   - **Response**: Deve conter `access_token`

---

## 🚀 Solução Automática

Use o script PowerShell para atualizar automaticamente:

```powershell
.\setup_ngrok.ps1
```

Ele irá:
1. ✅ Detectar a URL do ngrok
2. ✅ Atualizar `.env.local`
3. ✅ Atualizar `main.py` (CORS)

Depois reiniciar backend e frontend.

---

## 🔄 Fluxo Completo de Login

```
┌────────────────────────────────────────────────────┐
│ 1. User abre ngrok URL no navegador               │
│    https://abc123def45.ngrok.io:5173              │
└────────────────────────────────────────────────────┘
                        │
                        ▼
┌────────────────────────────────────────────────────┐
│ 2. Frontend carrega do .env.local                  │
│    VITE_API_BASE_URL=https://abc123def45.ngrok.io │
└────────────────────────────────────────────────────┘
                        │
                        ▼
┌────────────────────────────────────────────────────┐
│ 3. User digita email: admin@pingchampions.com     │
│    User digita senha: admin123                    │
│    Clica "Entrar"                                 │
└────────────────────────────────────────────────────┘
                        │
                        ▼
┌────────────────────────────────────────────────────┐
│ 4. axios POST para:                              │
│    https://abc123def45.ngrok.io/users/login       │
└────────────────────────────────────────────────────┘
                        │
                        ▼
┌────────────────────────────────────────────────────┐
│ 5. ngrok encaminha para backend local:            │
│    http://127.0.0.1:8000/users/login              │
└────────────────────────────────────────────────────┘
                        │
                        ▼
┌────────────────────────────────────────────────────┐
│ 6. Backend valida credenciais ✅                  │
│    Retorna: { access_token, user }                │
└────────────────────────────────────────────────────┘
                        │
                        ▼
┌────────────────────────────────────────────────────┐
│ 7. ngrok retorna resposta ao frontend             │
│    Response 200 OK                                │
└────────────────────────────────────────────────────┘
                        │
                        ▼
┌────────────────────────────────────────────────────┐
│ 8. Frontend salva token em localStorage           │
│    Redireciona para /                             │
│    UserMenu exibe "Administrador" ✅              │
└────────────────────────────────────────────────────┘
```

---

## 📊 Tabela de Diagnóstico

| Problema | Causa | Solução |
|----------|-------|---------|
| **Email ou senha inválido** | URL backend errada | Verificar `.env.local` e `VITE_API_BASE_URL` |
| **CORS error** | ngrok URL não em allow_origins | Atualizar `main.py` |
| **Timeout ao fazer login** | ngrok não rodando | Executar `ngrok http 8000` |
| **Backend respondendo 200 mas frontend erro** | Versão antiga do frontend em cache | Fazer `npm run dev` novamente ou Ctrl+Shift+R no navegador |
| **URL do ngrok mudou** | ngrok reiniciou (URL temporária) | Atualizar `.env.local` com nova URL |

---

## 💡 Dicas Úteis

### Manter URL do ngrok Constante

Se usa ngrok frequentemente, considere comprar uma conta e usar um domínio reservado:

```powershell
ngrok http 8000 --domain=seu-dominio.ngrok.io
```

### Ver Todas as Requisições do ngrok

Abrir em navegador:
```
http://127.0.0.1:4040
```

Mostra todas as requisições HTTP/HTTPS passadas pelo ngrok em tempo real.

### Debug no Frontend

Adicionar log em `frontend/src/services/auth.js`:

```javascript
console.log('API Base URL:', import.meta.env.VITE_API_BASE_URL)
```

Abrir DevTools (F12) → Console e verificar qual URL está sendo usada.

---

## ❓ Ainda não funciona?

Criar um relatório com:

1. URL do ngrok: `https://...`
2. Erro exato recebido
3. Output de DevTools (F12 → Console)
4. Status do endpoint:
   ```powershell
   Invoke-WebRequest https://YOUR_NGROK_URL/users/login -Method POST ...
   ```
5. Verificar se ngrok está rodando:
   ```powershell
   Invoke-WebRequest http://127.0.0.1:4040/api/tunnels
   ```

---

**Última atualização**: 13 de Novembro de 2025
