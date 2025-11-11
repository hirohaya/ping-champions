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
- 🎮 **Match Recording**: Record match results with detailed game scores
- 🌐 **Internationalization**: Full support for Portuguese (BR) and English (US)
- 🏆 **Elo Rating System**: Automatic skill-based ranking calculation
- 📈 **Ranking System**: Automatic ranking with leaderboard view
- 📱 **Responsive UI**: Vue 3 frontend with modern styling
- 🔄 **RESTful API**: FastAPI backend with SQLAlchemy ORM
- 💾 **Persistent Storage**: SQLite database with Alembic migrations

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

## 🌐 Internationalization (i18n)

Ping Champions supports **Portuguese (BR)** and **English (US)** out of the box.

### Language Selection
- Click the language dropdown in the header to switch between languages
- Your preference is saved automatically to browser localStorage
- The app auto-detects your browser language on first visit

### Supported Languages
- 🇧🇷 **Português (BR)** - Portuguese (Brazil)
- 🇺🇸 **English (US)** - English (United States)

### For Developers
See **[I18N_CONFIG.md](./I18N_CONFIG.md)** for detailed documentation on:
- How to add new translations
- Using the i18n system in Vue components
- Backend message localization API
- Extending to new languages

### Backend i18n API
```
GET  /api/i18n/locales              # Get available languages
GET  /api/i18n/messages             # Get localized messages
POST /api/i18n/set-locale           # Set preferred language
```

---

## 📁 Project Structure

```
ping-champions/
├── .github/
│   └── copilot-instructions.md # AI agent guidance
│
├── backend/                    # FastAPI backend
│   ├── main.py                # Entry point
│   ├── i18n.py                # Internationalization utilities
│   ├── database.py            # Database configuration
│   ├── models/                # SQLAlchemy models
│   ├── routers/
│   │   ├── i18n.py            # i18n API endpoints
│   │   └── ...                # Other endpoints
│   ├── requirements.txt        # Python dependencies
│   └── README.md              # Backend documentation
│
├── frontend/                  # Vue 3 + Vite frontend
│   ├── src/
│   │   ├── components/
│   │   │   └── LanguageSwitcher.vue  # Language selector
│   │   ├── locales/           # Translation files
│   │   │   ├── pt-BR.json     # Portuguese translations
│   │   │   └── en-US.json     # English translations
│   │   ├── i18n.js            # i18n configuration
│   │   ├── services/
│   │   │   └── translation.js # Translation API service
│   │   ├── views/             # Page components
│   │   └── router/            # Route configuration
│   ├── package.json           # Node dependencies (includes vue-i18n)
│   └── README.md              # Frontend documentation
│
├── I18N_CONFIG.md             # Internationalization guide
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

### Sprint 4: Testing & Migrations ✅ COMPLETED (Nov 10)
- ✅ **Task 1**: vitest setup for Vue 3 component testing
  - Installed vitest, @vue/test-utils, @testing-library/vue, jsdom
  - Created vitest.config.js with coverage configuration
  - Component tests for EventCard, Breadcrumbs, API service
  - **17 tests passing** with proper Vue Router integration
  - Added npm scripts: `test`, `test:ui`, `test:coverage`
- ✅ **Task 2**: Alembic migrations framework
  - Initialized Alembic with autogenerate enabled
  - Created initial migration for events, players, matches tables
  - Configured env.py with model imports and auto-detection
  - Migration applied successfully: database created with proper schema
  - Added Alembic commands documentation to README
- ✅ **Task 3**: Elo rating system and high-priority frontend features
  - Implemented complete Elo rating calculation backend (54 tests passing)
  - Built RankingView.vue with leaderboard, medals, and sorting
  - Built MatchHistoryView.vue with match history and rating changes
  - Created PlayerStatistics.vue component with stats display
  - Enhanced PlayersView.vue with Elo ratings and wins counter
  - **92.25% test coverage**, all endpoints validated

### Sprint 5: High-Priority Frontend Features ✅ COMPLETED (Nov 10)
- ✅ **Display Elo on Player List**: Purple gradient badges showing current rating
- ✅ **Display Elo on Ranking View**: Complete leaderboard with medals, sorting, win rate
- ✅ **Create Match History View**: Cards showing match results with ±Elo changes
- ✅ **Add Player Statistics Component**: Win/loss record, win rate %, progress bar
- ✅ **Fix API endpoints**: Corrected all frontend service layer calls to match backend
- ✅ **All 54 backend tests passing** with no integration issues

### Sprint 6: Internationalization & Score Recording ✅ COMPLETED (Nov 10)
- ✅ **Match Score Recording**: Added player1_games, player2_games, games_score fields
  - Backend: Extended Match model with 3 new columns
  - Frontend: Two-step form (Step 1: Create match, Step 2: Add sets won)
  - Modal interface for optional detailed game scores
  - Database migration: f4d825fe9491
- ✅ **Comprehensive i18n System**: Portuguese (BR) and English (US)
  - Frontend: Installed vue-i18n, created locale files with 50+ translation keys
  - Backend: Implemented Messages class, i18n router with 3 API endpoints
  - Language Switcher component in header with auto-detection
  - All 54 tests passing with i18n support
  - Complete documentation in I18N_CONFIG.md

---

## 🎯 Development Workflow

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

## �️ Database Migrations

Migrations are managed with **Alembic**. The database schema is version-controlled through migration files.

### Migration Commands

**Create a new migration** (when schema changes):
```bash
cd backend
alembic revision --autogenerate -m "Description of changes"
```

**Apply migrations to database**:
```bash
cd backend
alembic upgrade head              # Apply all pending migrations
alembic upgrade +1                # Apply next migration
alembic downgrade -1              # Revert last migration
```

**Check migration status**:
```bash
cd backend
alembic current                   # Show current revision
alembic history                   # Show migration history
```

**Configuration**: `backend/alembic.ini`
- Database URL: `sqlite:///pingchampions.db`
- Migration scripts: `backend/migrations/versions/`
- Auto-detected changes: Table/column additions, deletions, modifications

### First-Time Setup

The database is automatically initialized when running the backend for the first time. No manual migration needed.

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
✅ **Sprint 4 Completed**: Testing & migrations (Nov 10, 2025)
  - Elo rating system: 54 tests passing, 92.25% coverage
  - Alembic migrations: Configured and working
  - vitest setup: 17 tests passing
✅ **Sprint 5 Completed**: High-priority frontend features (Nov 10, 2025)
  - ✅ Elo display on player list (with gradient badges)
  - ✅ Leaderboard ranking view (with medals and sorting)
  - ✅ Match history view (with rating changes)
  - ✅ Player statistics component (reusable)
  - ⏳ E2E tests with Playwright (selectors need adjustment)

---

## 📞 Development Support

See `.github/copilot-instructions.md` for AI agent context and architecture decisions.

See `docs/TASKS.md` for detailed task list and prioritization.
🟡 **Sprint 2 In Progress**: API Contracts & Validation (Nov 10, 2025)  
⏳ **Next**: Sprint 3 - Infrastructure (linting, tests, migrations)

---

**Quick start**: Run `python setup.py` to get started.
