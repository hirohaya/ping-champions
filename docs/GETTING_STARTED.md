# 🚀 Quick Start Guide - Ping Champions

Welcome to **Ping Champions** — a Table Tennis Tournament Management System!

This guide will get you up and running in minutes.

---

## ⚡ Fastest Way to Get Started

### One-Line Setup (Recommended)
```powershell
python setup.py
```

That's it! This script will:
1. ✅ Create Python virtual environment
2. ✅ Install all backend dependencies
3. ✅ Install all frontend dependencies
4. ✅ Create configuration files
5. ✅ Show you the next steps

**Works on**: Windows, macOS, Linux

---

## 🎮 Start Development Servers

### Terminal 1: Backend Server
```powershell
python run_backend.py
```
- API runs on: **http://127.0.0.1:8000**
- Swagger docs at: **http://127.0.0.1:8000/docs**

### Terminal 2: Frontend Server
```powershell
cd frontend
npm run dev
```
- App runs on: **http://localhost:5173**
- Open this in your browser and start creating tournaments!

---

## 📋 Main Features

✅ **Create Events** - Organize tournaments  
✅ **Manage Players** - Register participants  
✅ **Record Matches** - Track game results  
✅ **Auto Rankings** - Elo rating calculations  
✅ **Multi-Language** - Portuguese (BR) & English  
✅ **Responsive** - Desktop, tablet, mobile  

---

## 🛠️ Useful Commands

### Backend
```bash
# Run tests
cd backend
pytest

# Check code quality
python -m ruff check .

# Reset database
python recreate_db.py
```

### Frontend
```bash
# Run tests
cd frontend
npm test

# Check code quality
npm run lint

# Build for production
npm run build
```

---

## 📚 Documentation

- **Full Guide**: See `README.md`
- **Backend Code**: See `backend/README.md`
- **Frontend Code**: See `frontend/README.md`
- **AI Context**: See `.github/copilot-instructions.md`

---

## 🐛 Troubleshooting

### Python not found?
Install from: https://www.python.org/downloads/

### Node not found?
Install from: https://nodejs.org/

### Port already in use?
- Change backend port in `run_backend.py`
- Change frontend port with `npm run dev -- --port 3000`

### Database errors?
```bash
python recreate_db.py
```

---

## 🎯 Next Steps

1. **Create an Event**
   - Go to Events → Create Event
   - Fill in name, date, time

2. **Add Players**
   - Go to your event → Players
   - Register tournament participants

3. **Record Matches**
   - Go to your event → Matches
   - Create matches and record results

4. **Check Rankings**
   - Go to Rankings
   - See updated Elo ratings

---

## 💡 Tips

- 🌐 **Switch Language**: Click the language dropdown in the header
- 🔄 **Auto Save**: Changes save automatically
- 📱 **Mobile Friendly**: Works great on phones and tablets
- 🎨 **Light/Dark**: Theme follows your system settings

---

## 🤝 Contributing

Want to help? See `README.md` for contribution guidelines.

---

## 📞 Support

Questions? Check the documentation or see `.github/copilot-instructions.md` for architecture details.

---

**Ready to get started?**

```powershell
python setup.py
```

Then open **http://localhost:5173** in your browser! 🎉

