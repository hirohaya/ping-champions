# 🏓 Ping Champions

**Table Tennis Tournament Management System** — A modern web application for organizing ping pong events, managing players, recording matches, and tracking rankings.

[![GitHub](https://img.shields.io/badge/GitHub-hirohaya%2Fping--champions-blue?logo=github)](https://github.com/hirohaya/ping-champions)
[![License](https://img.shields.io/badge/License-MIT-green)]()
[![Python](https://img.shields.io/badge/Python-3.9+-blue?logo=python)]()
[![Node.js](https://img.shields.io/badge/Node.js-20+-green?logo=node.js)]()

---

## 📋 Quick Links

- **🚀 Get Started**: Run `python setup.py` (automated setup)
- **🤖 AI Agent Guide**: Read [`.github/copilot-instructions.md`](./.github/copilot-instructions.md)
- **🎯 Architecture Review**: [`ARCHITECTURE_REVIEW.md`](./ARCHITECTURE_REVIEW.md)

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
│   └── copilot-instructions.md # AI agent guidance (GitHub Copilot, Claude, etc.)
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
├── docs/                      # (Archived - see ARCHITECTURE_REVIEW.md)
│
├── setup.py                   # Unified project setup script
├── run_backend.py             # Quick backend startup
├── recreate_db.py             # Database reset utility
├── ARCHITECTURE_REVIEW.md     # Technical analysis
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
See [`ARCHITECTURE_REVIEW.md`](./ARCHITECTURE_REVIEW.md) for detailed roadmap.

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

This project includes a comprehensive **architecture review** with:
- ✅ Complexity analysis (currently **low**)
- ✅ Abstraction levels (2 layers; recommend service layer)
- ✅ Method responsibilities (well-focused)
- ✅ Growth potential (**medium/high** after base improvements)
- ✅ Maintainability scores (**medium** → **high** with suggested fixes)
- ✅ Onboarding difficulty (**medium** → **high** after Sprint 4)

**Key findings**:
- 5 critical issues (P0), 7 high-priority (P1), 10 medium (P2)
- 24 prioritized tasks with clear acceptance criteria
- 4-week realistic roadmap to production-ready state

👉 **Read full review**: [`ARCHITECTURE_REVIEW.md`](./ARCHITECTURE_REVIEW.md)

---

## 🤝 Contributing

1. Check [`ARCHITECTURE_REVIEW.md`](./ARCHITECTURE_REVIEW.md) for current priorities
2. Follow code style: PEP 8 (Python), ES6 (JavaScript)
3. Open an issue for bugs or features

---

## 📚 Documentation

| Document | Purpose | Read Time |
|----------|---------|-----------|
| [`ARCHITECTURE_REVIEW.md`](./ARCHITECTURE_REVIEW.md) | Technical analysis & roadmap | 20 min |
| [`.github/copilot-instructions.md`](./.github/copilot-instructions.md) | AI agent guidance | 10 min |

---

## 🐛 Known Issues

See [`ARCHITECTURE_REVIEW.md`](./ARCHITECTURE_REVIEW.md) for details:
- SFC error in EventsView.vue (T001)
- ORM relationship issues (T003)
- Inconsistent trailing slashes (T004)
- Missing Pydantic schemas (T006–T008)

---

## 📞 Support

- 🚀 **Setup not working?** → Run `python setup.py` again or check [`.github/copilot-instructions.md`](./.github/copilot-instructions.md)
- 🤖 **Need AI assistance?** → Read [`.github/copilot-instructions.md`](./.github/copilot-instructions.md) for full context
- ️ **Architecture & roadmap?** → Read [`ARCHITECTURE_REVIEW.md`](./ARCHITECTURE_REVIEW.md)

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
✅ **Initial documentation complete**: 9 files, ~8500 lines  
✅ **Setup automation complete**: Unified `setup.py` script (cross-platform)  
✅ **AI guidance added**: [`.github/copilot-instructions.md`](./.github/copilot-instructions.md)  
🟢 **Ready for Sprint 1**: Begin implementation now  
📍 **Estimated completion (MVP)**: ~4 weeks (Sprints 1–4)

---

**Quick start**: Run `python setup.py` to get started.
