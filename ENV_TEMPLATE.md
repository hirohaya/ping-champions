# Environment Configuration Template

## Backend (.env)

```
# Database
DATABASE_URL=sqlite:///./pingchampions.db

# Server
DEBUG=True
LOG_LEVEL=INFO

# CORS
CORS_ORIGINS=["http://localhost:5173", "http://localhost:3000"]

# API
API_TITLE=Ping Champions API
API_VERSION=0.1.0
```

## Frontend (.env.local)

```
# API Configuration
VITE_API_BASE_URL=http://localhost:8000
VITE_API_TIMEOUT=30000

# Debug
VITE_DEBUG=true
```

## Usage

1. **Backend**:
   - Copy `.env` to `backend/.env`
   - Update values conforme necessário
   - NÃO commit `.env` (já está em .gitignore)

2. **Frontend**:
   - Copy `.env.local` to `frontend/.env.local`
   - Update values conforme necessário
   - NÃO commit `.env.local` (já está em .gitignore)

## Production Setup

Para produção, usar variáveis de ambiente:

```bash
# Backend
export DATABASE_URL=postgresql://user:pass@host/db
export DEBUG=False
export CORS_ORIGINS=["https://example.com"]

# Frontend (buildtime)
export VITE_API_BASE_URL=https://api.example.com
```
