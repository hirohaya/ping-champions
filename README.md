# 🏓 Ping Champions

**Table Tennis Tournament Management System** — A modern web application for organizing ping pong events, managing players, recording matches, and tracking rankings.

[![GitHub](https://img.shields.io/badge/GitHub-hirohaya%2Fping--champions-blue?logo=github)](https://github.com/hirohaya/ping-champions)
[![License](https://img.shields.io/badge/License-MIT-green)]()
[![Python](https://img.shields.io/badge/Python-3.9+-blue?logo=python)]()
[![Node.js](https://img.shields.io/badge/Node.js-20+-green?logo=node.js)]()
[![Linting](https://img.shields.io/badge/Linting-Ruff%20+%20ESLint-brightgreen)]()

---

## 📋 Quick Links

- **🚀 Get Started**: Run `python setup.py` (automated setup)
- **📚 Development**: See [Development Workflow](#development-workflow)
- **📝 Tasks**: See `docs/TASKS.md` for prioritized feature list

---

## ✨ Features

- 🎉 **Event Management**: Create and organize tournaments
- 👥 **Player Registration**: Register players for events
- 🎮 **Match Recording**: Record match results and winners
- 📈 **Ranking System**: Automatic ranking calculation by score
- 📱 **Responsive UI**: Vue 3 frontend with modern styling
- 🔄 **RESTful API**: FastAPI backend with SQLAlchemy ORM
- 💾 **Persistent Storage**: SQLite database

---

## 🛠️ Tech Stack

### Backend
- **Framework**: FastAPI
- **ORM**: SQLAlchemy
- **Database**: SQLite
- **Language**: Python 3.9+
- **Linting**: Ruff (Python code quality)
- **Testing**: pytest (unit tests, fixtures configured)

### Frontend
- **Framework**: Vue 3 (Composition API)
- **Build Tool**: Vite
- **Router**: Vue Router
- **HTTP Client**: Axios
- **Language**: JavaScript (ES6+)
- **Linting**: ESLint with Vue 3 plugin (all passing)
- **Package Manager**: npm

---

## 🚀 Quick Start

### Prerequisites
- Python 3.9+ and `pip`
- Node.js 20+ and `npm`
- Git

### Automated Setup (Recommended)
```powershell
python setup.py
```

This script automatically:
1. Creates Python virtual environment
2. Installs backend dependencies
3. Installs frontend dependencies
4. Creates `.env` and `.env.local` files
5. Shows next steps

**Cross-platform**: Supports Windows, macOS, and Linux.

### Manual Setup (Alternative)

**Backend**:
```powershell
cd backend
python -m venv venv
.\venv\Scripts\activate          # Windows
# or: source venv/bin/activate   # macOS/Linux

pip install -r requirements.txt
python run_backend.py
```
**Frontend**:
```powershell
cd frontend
npm install
npm run dev
```

### Database Reset
```powershell
python recreate_db.py
```

**⚠️ Warning**: This deletes all data and recreates the schema.

---

## 📁 Project Structure

```
ping-champions/
├── .github/
│   └── copilot-instructions.md # AI agent guidance
│
├── backend/                    # FastAPI backend
│   ├── main.py                # Entry point
│   ├── database.py            # Database configuration
│   ├── models/                # SQLAlchemy models
│   ├── routers/               # API endpoints
│   ├── requirements.txt        # Python dependencies
│   └── README.md              # Backend documentation
│
├── frontend/                  # Vue 3 + Vite frontend
│   ├── src/
│   │   ├── components/        # Reusable Vue components
│   │   ├── views/             # Page components
│   │   ├── services/          # API integration
│   │   └── router/            # Route configuration
│   ├── package.json           # Node dependencies
│   └── README.md              # Frontend documentation
│
├── setup.py                   # Unified project setup script
├── run_backend.py             # Quick backend startup
├── recreate_db.py             # Database reset utility
```

---

## 📈 Development Roadmap

### Sprint 1: Quick Wins ✅ COMPLETED (Nov 3)
- ✅ Fixed SFC error in EventsView.vue (T001)
- ✅ Fixed ORM relationship issues (T003)
- ✅ Standardized API trailing slashes (T004)

### Sprint 2: API Contracts ✅ COMPLETED (Nov 10)
- ✅ Added comprehensive Pydantic validation schemas
- ✅ Added docstrings to all endpoints with Swagger documentation
- ✅ Tested all validation rules and constraints

### Sprint 3: Infrastructure ✅ COMPLETED (Nov 10)
- ✅ **Task 1**: Fixed 93 Ruff linting errors in backend
  - E712: Changed `== True` comparisons to boolean truthiness
  - W293: Removed whitespace from blank lines
  - N805: Fixed Pydantic validators with `@classmethod`
  - B008: Documented FastAPI `Depends()` pattern (intentional)
  - `ruff check .` now passes: **All checks passed!**
- ✅ **Task 2**: Created pytest framework
  - conftest.py with database fixtures
  - Test suites for events, players, matches, ranking
  - 850+ lines of test code ready (fixture debugging in progress)
- ✅ **Task 3**: Setup ESLint for frontend
  - Installed ESLint with Vue 3 plugin support
  - Created eslint.config.js with flat config format
  - Fixed all code issues: **0 errors, 0 warnings**
  - Added `npm run lint` script for automated linting

### Sprint 4: Testing & Migrations (In Progress)
- ✅ **Task 1**: vitest setup for Vue 3 component testing
  - Installed vitest, @vue/test-utils, @testing-library/vue, jsdom
  - Created vitest.config.js with coverage configuration
  - Component tests for EventCard, Breadcrumbs, API service
  - **17 tests passing** with proper Vue Router integration
  - Added npm scripts: `test`, `test:ui`, `test:coverage`
- Task 2: Alembic migrations framework
- Task 3: Full test coverage and documentation

---

## � Development Workflow

### Starting Development Servers

**Terminal 1 - Backend**:
```bash
python run_backend.py
# Server runs on: http://127.0.0.1:8000
# API Docs at: http://127.0.0.1:8000/docs (Swagger UI)
```

**Terminal 2 - Frontend**:
```bash
cd frontend
npm run dev
# App runs on: http://localhost:5173
```

Both servers support hot-reload for development.

### Running Code Quality Checks

**Backend Linting**:
```bash
cd backend
python -m ruff check .              # Check issues
python -m ruff check . --fix        # Auto-fix
```

**Frontend Linting**:
```bash
cd frontend
npm run lint                        # Check and fix
```

### Running Tests

**Backend Tests** (pytest):
```bash
cd backend
pytest                              # Run all tests
pytest -v                           # Verbose output
pytest --cov                        # With coverage report
```

**Frontend Tests** (vitest):
```bash
cd frontend
npm test                            # Run tests in headless mode
npm run test:ui                     # Run with interactive UI
npm run test:coverage               # Run with coverage report
```

---

## �🔧 Linting & Code Quality

### Backend (Ruff)
```bash
cd backend
python -m ruff check .          # Check linting
python -m ruff check . --fix    # Auto-fix issues
```

**Configuration**: `backend/pyproject.toml`
- Target: Python 3.9+
- Line length: 100 characters
- Rules: E, W, F, I, N, UP, B, C90 (McCabe complexity)
- Ignores: E501 (line length), E203 (whitespace), B008 (FastAPI pattern)

### Frontend (ESLint)
```bash
cd frontend
npm run lint                    # Check and fix linting
```

**Configuration**: `frontend/eslint.config.js`
- Format: ESLint v9 flat config
- Parser: Built-in ES2021
- Plugins: Vue 3, Prettier
- Status: ✅ **All passing** (0 errors, 0 warnings)

---

## 👨‍💻 Author

**Lucas Hiroshi Hayashida** (hirohaya)  
GitHub: [@hirohaya](https://github.com/hirohaya)

---

## 🎉 Status

✅ **Repository created**: November 2, 2025  
✅ **Setup automation complete**: Unified `setup.py` script (cross-platform)  
✅ **Sprint 1 Completed**: Critical bugs fixed (Nov 3, 2025)  
✅ **Sprint 2 Completed**: API contracts with validation (Nov 10, 2025)  
✅ **Sprint 3 Completed**: Infrastructure setup (Nov 10, 2025)
  - Ruff linting: All 93 errors fixed
  - ESLint frontend: All passing
  - pytest fixtures: Created and documented  
🟡 **Sprint 4 In Progress**: Testing & migrations

---

## 📞 Development Support

See `.github/copilot-instructions.md` for AI agent context and architecture decisions.

See `docs/TASKS.md` for detailed task list and prioritization.
🟡 **Sprint 2 In Progress**: API Contracts & Validation (Nov 10, 2025)  
⏳ **Next**: Sprint 3 - Infrastructure (linting, tests, migrations)

---

**Quick start**: Run `python setup.py` to get started.
