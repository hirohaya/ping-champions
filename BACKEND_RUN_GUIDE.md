# Backend Execution Guide

## ✅ Backend Running Successfully!

**Server**: http://127.0.0.1:8000  
**Status**: Ready for requests  
**Mode**: Development with auto-reload

## 🚀 How to Run Backend

### Option 1: Using Python Script (Recommended) ⭐
```powershell
cd c:\Users\hiros\OneDrive\Documents\ping-champions
python run_backend.py
```

**Why this works:**
- ✅ Automatically sets Python path correctly
- ✅ No import errors
- ✅ Auto-reload enabled
- ✅ Simplest approach

### Option 2: Direct Uvicorn from Root
```powershell
cd c:\Users\hiros\OneDrive\Documents\ping-champions
python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

### Option 3: Activate venv then run
```powershell
cd c:\Users\hiros\OneDrive\Documents\ping-champions
.\venv\Scripts\Activate.ps1
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

## ❌ What NOT to Do

```powershell
# ❌ WRONG - Running from backend directory
cd backend
python -m uvicorn backend.main:app  # ModuleNotFoundError: No module named 'backend'
```

**Why it fails:**
- ❌ Python can't find `backend` module when already inside it
- ❌ Import path is incorrect
- ❌ Uvicorn looks for `backend.main` from current directory

## 📝 Key Points

| Command | Location | Status |
|---------|----------|--------|
| `python run_backend.py` | Root dir | ✅ Works |
| `python -m uvicorn backend.main:app` | Root dir | ✅ Works |
| `python -m uvicorn backend.main:app` | backend/ dir | ❌ Fails |

## 🔗 API Endpoints

Once running, access:
- **Base URL**: http://localhost:8000
- **API Documentation (Swagger)**: http://localhost:8000/docs
- **Alternative Docs (ReDoc)**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/

## 📦 Backend Routes

- `GET /` - Root endpoint
- `GET /events` - List events
- `GET /players` - List players
- `GET /matches` - List matches
- `GET /ranking` - Get ranking

See http://localhost:8000/docs for full API documentation.

## 🛑 Stop Backend

Press `CTRL+C` in the terminal running the backend.

---

**Remember**: Always run from the **root project directory**, not from inside `backend/`
