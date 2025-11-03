# 🏓 Ping Champions

**Table Tennis Tournament Management System** — A modern web application for organizing ping pong events, managing players, recording matches, and tracking rankings.

[![GitHub](https://img.shields.io/badge/GitHub-hirohaya%2Fping--champions-blue?logo=github)](https://github.com/hirohaya/ping-champions)
[![License](https://img.shields.io/badge/License-MIT-green)]()
[![Python](https://img.shields.io/badge/Python-3.9+-blue?logo=python)]()
[![Node.js](https://img.shields.io/badge/Node.js-20+-green?logo=node.js)]()

---

## 📋 Quick Links

- **🚀 Get Started**: Run `python setup.py` (automated setup)

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

### Frontend
- **Framework**: Vue 3
- **Build Tool**: Vite
- **Router**: Vue Router
- **HTTP Client**: Axios
- **Language**: JavaScript (ES6+)

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

Backend runs on: **http://127.0.0.1:8000**  
Swagger UI: **http://127.0.0.1:8000/docs**

**Frontend**:
```powershell
cd frontend
npm install
npm run dev
```

Frontend runs on: **http://localhost:5173**

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
└── 00_READ_ME_FIRST.md        # Start here (2 min)
```

---

## 🎯 Current Status

### ✅ Implemented
- Event CRUD operations (create, list, soft delete)
- Player registration and management
- Match recording (basic)
- Ranking endpoint
- Frontend pages (events, players, matches, ranking)
- Breadcrumb navigation

### 🔄 In Progress (Sprint 1–4)
Check implementation roadmap in the code.

**Next Priority (Sprint 1)**:
1. Fix SFC error in EventsView.vue
2. Standardize API trailing slashes
3. Add Pydantic schemas for validation
4. Configure linting and tests

---

## 📈 Development Roadmap

### Sprint 1: Quick Wins (1-2 days)
- Fix critical bugs
- Standardize API
- Remove dead code

### Sprint 2: API Contracts (2-3 days)
- Add Pydantic schemas
- Validate requests/responses
- Document Swagger

### Sprint 3: Infrastructure (2-3 days)
- Setup linting (Ruff, ESLint)
- Add unit tests (pytest, vitest)
- Configure migrations (Alembic)

### Sprint 4: Documentation (1-2 days)
- Complete API documentation
- Onboarding guides
- Contributing guidelines

### Sprint 5+: Features
- Match scoring & ranking logic
- Admin authentication
- Pagination & filtering
- CI/CD pipeline

---

## 📊 Assessment & Findings

This project is in **MVP phase**:
- 5 critical issues (P0), 7 high-priority (P1), 10 medium (P2)
- 24 prioritized tasks with clear acceptance criteria
- 4-week realistic roadmap to production-ready state

---

## 🤝 Contributing

1. Check [`ARCHITECTURE_REVIEW.md`](./ARCHITECTURE_REVIEW.md) for current priorities
2. Follow code style: PEP 8 (Python), ES6 (JavaScript)
3. Open an issue for bugs or features

---

## 📚 Documentation

- Core setup: `setup.py` script
- Backend: `backend/` folder
- Frontend: `frontend/` folder

---

## 🐛 Known Issues

- SFC error in EventsView.vue (T001)
- ORM relationship issues (T003)
- Inconsistent trailing slashes (T004)
- Missing Pydantic schemas (T006–T008)

---

## 📞 Support

- 🚀 **Setup not working?** → Run `python setup.py` again
- 🐍 **Backend issues?** → Check `backend/` folder or test with Swagger UI at `http://127.0.0.1:8000/docs`
- ⚙️ **Frontend issues?** → Check `frontend/` folder or test at `http://localhost:5173`

---

## 📄 License

MIT License — see LICENSE file for details.

---

## 👨‍💻 Author

**Lucas Hiroshi Hayashida** (hirohaya)  
GitHub: [@hirohaya](https://github.com/hirohaya)

---

## 🎉 Status

✅ **Repository created**: November 2, 2025  
✅ **Setup automation complete**: Unified `setup.py` script (cross-platform)  
🟢 **Ready for development**: Begin Sprint 1 implementation

---

**Quick start**: Run `python setup.py` to get started.
