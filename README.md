# 🏓 Ping Champions

Manage table tennis tournaments. Create events, register players, record matches, and track rankings with Elo ratings.

## 📚 Documentation Index

### 🚀 Getting Started
- **[Quick Start ngrok](docs/QUICK_START_NGROK.txt)** - Setup with public URL in < 1 minute
- **[Setup Complete](docs/SETUP_NGROK_COMPLETO.md)** - Full ngrok setup guide
- **[ngrok Guide](docs/GUIA_NGROK.md)** - Complete ngrok reference

### 🛠️ Setup & Installation
```powershell
# Initial setup (Python + Node dependencies)
python setup.py

# Run backend
python run_backend.py

# Run frontend
cd frontend && npm run dev

# With ngrok (public URL)
.\scripts\init_project_simple.ps1
```

### 📦 Project Structure

```
ping-champions/
├── 📁 backend/                      # FastAPI backend
│   ├── models/                      # SQLAlchemy ORM models
│   ├── routers/                     # API endpoints
│   ├── tests/                       # Backend unit & integration tests
│   ├── utils/                       # Utilities (bracket generator, ELO, etc)
│   └── main.py                      # FastAPI app entry point
│
├── 📁 frontend/                     # Vue 3 + Vite frontend
│   ├── src/                         # Vue components & pages
│   ├── e2e/                         # Playwright E2E tests
│   └── package.json                 # Node dependencies
│
├── 📁 tests/                        # Project-wide tests
│   ├── unit/                        # Unit tests
│   ├── integration/                 # Integration tests
│   └── e2e/                         # End-to-end tests
│
├── 📁 scripts/                      # Initialization & utility scripts
│   ├── init_project_simple.ps1      # Auto-start (Backend → Frontend → ngrok)
│   ├── init_project_with_ngrok.ps1  # Advanced initialization
│   └── start_ngrok.ps1              # ngrok startup helper
│
├── 📁 docs/                         # Documentation & guides
│   ├── QUICK_START_NGROK.txt        # Quick reference
│   ├── SETUP_NGROK_COMPLETO.md      # Complete setup guide
│   ├── GUIA_NGROK.md                # ngrok reference
│   └── [18+ other guides]           # Sprint docs, status, guides
│
├── 🔧 Core Files (Root)
│   ├── run_backend.py               # Backend startup script
│   ├── setup.py                     # Project initialization
│   ├── recreate_db.py               # Database reset utility
│   ├── debug_backend.py             # Debug utilities
│   └── README.md                    # This file
│
└── 🗄️ Database
    └── pingchampions.db             # SQLite database (auto-created)
```

## ⚡ Quick Commands

### Initialize Project
```powershell
# Setup everything (one time)
python setup.py

# Auto-start all services with ngrok
.\scripts\init_project_simple.ps1
```

### Development
```powershell
# Terminal 1: Backend (http://127.0.0.1:8000)
python run_backend.py

# Terminal 2: Frontend (http://localhost:5173)
cd frontend && npm run dev

# Terminal 3: ngrok (https://xyz.ngrok.io)
ngrok http 5173
```

### Testing
```powershell
# Backend unit tests
pytest tests/unit/test_tournament.py -v

# Frontend E2E tests
cd frontend && npx playwright test e2e/tournaments.spec.js

# All tests
pytest tests/ && cd frontend && npx playwright test
```

### Database
```powershell
# Reset database (⚠️ deletes all data)
python recreate_db.py

# Debug database
python debug_backend.py
```

## 🧪 Test Status

| Suite | Tests | Status |
|-------|-------|--------|
| Unit (Tournament) | 17/17 | ✅ 100% |
| Integration API | 14/14 | ✅ 100% |
| E2E (Tournament) | 14/14 | ✅ 100% |
| **Total** | **45/45** | **✅ 100%** |

## 📡 API Documentation

When backend is running, visit:
- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc

## 🌐 Deploy with ngrok

Share your local app globally:

```powershell
# Simple (free, random URL)
ngrok http 5173

# Fixed subdomain (requires ngrok Pro)
ngrok http --url=your-domain.ngrok-free.dev 5173
```

See [docs/SETUP_NGROK_COMPLETO.md](docs/SETUP_NGROK_COMPLETO.md) for details.

## 🛠️ Tech Stack

- **Backend**: FastAPI, SQLAlchemy, SQLite, Pydantic
- **Frontend**: Vue 3, Vite, Vue Router, Axios
- **Database**: SQLite (file-based)
- **Testing**: pytest, Playwright, vitest
- **Quality**: Ruff linter, ESLint
- **i18n**: vue-i18n (EN, PT-BR)
- **DevTools**: ngrok, Playwright, pip, npm

## 🎯 Key Features

- ✅ Tournament management (Single Elimination, Swiss, Round Robin, Group+Knockout)
- ✅ Player registration with Elo ratings
- ✅ Match recording and result tracking
- ✅ Automatic ranking calculation
- ✅ Bracket generation
- ✅ Internationalization (EN, PT-BR)
- ✅ Event management
- ✅ Public URL sharing (via ngrok)

## 📖 Documentation

All documentation is in `docs/` folder:

- **[QUICK_START_NGROK.txt](docs/QUICK_START_NGROK.txt)** - Quick reference guide
- **[INIT_WITH_NGROK.md](docs/INIT_WITH_NGROK.md)** - Step-by-step initialization
- **[SETUP_NGROK_COMPLETO.md](docs/SETUP_NGROK_COMPLETO.md)** - Complete guide with FAQs
- **[GUIA_NGROK.md](docs/GUIA_NGROK.md)** - ngrok universal reference
- **[SPRINT3_TEST_RESULTS.md](docs/SPRINT3_TEST_RESULTS.md)** - Test results & validation
- Plus 15+ additional guides for development, testing, and deployment

## 🔗 Repository

https://github.com/hirohaya/ping-champions

## 📄 License

MIT License - See LICENSE file for details

## 🚀 Getting Help

1. Check `docs/` folder for guides
2. Run `.\scripts\init_project_simple.ps1` for auto-setup
3. See ngrok dashboard at http://127.0.0.1:4040 (while running)
4. Check test results in `docs/SPRINT3_TEST_RESULTS.md`

---

**Last Updated**: November 13, 2025  
**Version**: Sprint 3 (Tournament Feature - 100% Tests Passing)  
**Status**: ✅ Production Ready