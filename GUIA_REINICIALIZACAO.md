# Guia de Reinicialização - Frontend e Backend

## Status Atual
- **Frontend**: ✅ Rodando em `http://localhost:5173` (npm)
- **Backend**: ✅ Rodando em `http://127.0.0.1:8000` (Python/FastAPI)

## Como Reinicializar

### Se o Backend Cair

Use o mesmo PowerShell/prompt que já está sendo usado:

```powershell
cd c:\Users\hiros\OneDrive\Documents\ping-champions
python run_backend.py
```

**Resultado esperado**:
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

### Se o Frontend Cair

Use o mesmo PowerShell/prompt:

```powershell
cd c:\Users\hiros\OneDrive\Documents\ping-champions\frontend
npm run dev
```

**Resultado esperado**:
```
  ➜  Local:   http://localhost:5173/
```

### Se Ambos Cairem

1. **Terminal 1 - Backend**:
   ```powershell
   cd c:\Users\hiros\OneDrive\Documents\ping-champions
   python run_backend.py
   ```

2. **Terminal 2 - Frontend**:
   ```powershell
   cd c:\Users\hiros\OneDrive\Documents\ping-champions\frontend
   npm run dev
   ```

## Verificar Status

### Processo Python (Backend)
```powershell
Get-Process python -ErrorAction SilentlyContinue | Select-Object Name, Id
```

### Processos Node (Frontend)
```powershell
Get-Process node -ErrorAction SilentlyContinue | Select-Object Name, Id
```

## Matar Processos (Se Necessário)

### Matar todos os Node
```powershell
Get-Process node -ErrorAction SilentlyContinue | Stop-Process -Force
```

### Matar Python Backend
```powershell
Get-Process python -ErrorAction SilentlyContinue | Stop-Process -Force
```

### Matar Tudo
```powershell
Get-Process python -ErrorAction SilentlyContinue | Stop-Process -Force
Get-Process node -ErrorAction SilentlyContinue | Stop-Process -Force
```

## URLs de Acesso

| Serviço | URL | Tipo |
|---------|-----|------|
| Frontend | `http://localhost:5173` | Web UI Vue |
| Backend API | `http://127.0.0.1:8000` | FastAPI |
| Swagger Docs | `http://127.0.0.1:8000/docs` | API Docs |
| ReDoc | `http://127.0.0.1:8000/redoc` | API Docs (ReDoc) |

## Portas em Uso

- **5173**: Frontend (Vite Dev Server)
- **8000**: Backend (FastAPI/Uvicorn)

## Troubleshooting

### "Port already in use"
Se a porta já está em uso, mate o processo e reinicie:

```powershell
# Matar e reiniciar frontend
Get-Process node | Stop-Process -Force
cd frontend && npm run dev

# Matar e reiniciar backend
Get-Process python | Stop-Process -Force
cd .. && python run_backend.py
```

### Backend não conecta ao banco de dados
1. Verifique se `backend/pingchampions.db` existe
2. Se não existir, execute: `python recreate_db.py`
3. Reinicie o backend: `python run_backend.py`

### Frontend não conecta ao backend
1. Verifique se backend está em `http://127.0.0.1:8000`
2. Abra DevTools (F12) → Console
3. Procure por erros de conexão
4. Reinicie backend: `python run_backend.py`

## Hotkeys no Vite (Frontend)

Enquanto o Vite está rodando:
- `h + Enter`: Mostrar ajuda
- `r + Enter`: Reload
- `c + Enter`: Clear console
- `q + Enter`: Quit

## Hotkeys no Uvicorn (Backend)

- `CTRL+C`: Parar o servidor
- `CTRL+Z`: Suspender (não recomendado)

---

**Última atualização**: 13 de Novembro de 2025
**Status**: ✅ Frontend e Backend rodando
**Branch**: `test-fixes-e2e`
