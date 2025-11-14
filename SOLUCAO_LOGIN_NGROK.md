# Resolvendo Problema de Login via ngrok

## Problema
Ao acessar a aplicação via ngrok, recebe erro "Email ou senha inválido" mesmo com credenciais corretas.

## Causa Raiz
O frontend estava com a URL da API hardcoded como `http://localhost:8000`, que não funciona quando acessado via ngrok.

## Solução Aplicada

### 1. Atualizar `api.js` para usar variável de ambiente ✅

**Arquivo**: `frontend/src/services/api.js`

**Antes**:
```javascript
const api = axios.create({
  baseURL: "http://localhost:8000"
});
```

**Depois**:
```javascript
const baseURL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";
const api = axios.create({
  baseURL: baseURL,
});
```

### 2. Configurar `.env.local` para ngrok

**Arquivo**: `frontend/.env.local`

Abra este arquivo e atualize com sua URL do ngrok:

```bash
# Para desenvolvimento local
VITE_API_BASE_URL=http://localhost:8000

# Para ngrok (substitua YOUR_NGROK_URL pela sua URL real)
# VITE_API_BASE_URL=https://YOUR_NGROK_URL.ngrok.io
```

## Como Obter Sua URL do ngrok

1. Se ngrok está rodando, procure na saída algo como:
   ```
   Forwarding    https://abc123def45.ngrok.io -> http://127.0.0.1:8000
   ```

2. Sua URL do ngrok é: `https://abc123def45.ngrok.io`

## Passo a Passo para Usar ngrok

### Opção 1: Desenvolvimento Local (padrão)
Não fazer nada, deixar como está. O frontend vai usar `http://localhost:8000`

### Opção 2: Usar ngrok
1. Iniciar ngrok para o backend:
   ```powershell
   ngrok http 8000
   ```

2. Copiar a URL fornecida (ex: `https://abc123def45.ngrok.io`)

3. Atualizar `frontend/.env.local`:
   ```bash
   VITE_API_BASE_URL=https://abc123def45.ngrok.io
   ```

4. Reiniciar o frontend:
   ```powershell
   cd frontend
   npm run dev
   ```

5. Acessar via ngrok URL do frontend (ex: `https://xyz789abc12.ngrok.io:5173`)

## ⚠️ IMPORTANTE: CORS

Se você receber erro de CORS, é porque o backend precisa permitir a URL do ngrok.

### Verificar Configuração CORS no Backend

**Arquivo**: `backend/main.py`

Procure por:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[...],
    ...
)
```

### Se ngrok não estiver na lista, adicionar:

```python
allow_origins=[
    "http://localhost:5173",
    "http://localhost:5174",
    "https://*.ngrok.io",  # Permite todos os ngrok
    # Ou específico:
    "https://abc123def45.ngrok.io"
]
```

## Testar Conexão

### Teste 1: Via curl (backend local)
```bash
curl -X POST http://127.0.0.1:8000/users/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@pingchampions.com","password":"admin123"}'
```

Resposta esperada: HTTP 200 com token JWT

### Teste 2: Via ngrok
```bash
curl -X POST https://YOUR_NGROK_URL.ngrok.io/users/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@pingchampions.com","password":"admin123"}'
```

## Credenciais de Teste

```
Email: admin@pingchampions.com
Senha: admin123

Email: organizador@pingchampions.com
Senha: org123

Email: jogador1@pingchampions.com
Senha: player1
```

## Próximas Verificações

1. ✅ Atualizado `frontend/src/services/api.js` para usar variável de ambiente
2. ⏳ Reiniciar frontend (npm run dev)
3. ⏳ Atualizar `.env.local` com URL ngrok (se necessário)
4. ⏳ Verificar CORS no backend (se necessário)
5. ⏳ Testar login novamente

## Se o Problema Persistir

1. Abra DevTools (F12) no navegador
2. Vá à aba "Network"
3. Tente fazer login
4. Procure pela requisição POST `/users/login`
5. Verificar:
   - URL usada
   - Status code
   - Response
   - Headers (verificar Authorization)

## Resumo das Mudanças

- ✅ `frontend/src/services/api.js` - Agora usa `VITE_API_BASE_URL`
- ✅ `frontend/.env.local` - Já tinha a variável (precisa atualizar)
- ⏳ Reiniciar frontend para aplicar mudanças
