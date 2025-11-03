@echo off
REM Development environment setup script for Trunk-Based Development
REM For Windows PowerShell/CMD

setlocal enabledelayedexpansion

echo.
echo ========================================
echo   Setting up Ping Champions
echo ========================================
echo.

REM Backend Setup
echo.
echo === Backend Setup ===
echo.

cd backend

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
) else (
    echo Virtual environment exists
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing backend dependencies...
pip install -r requirements.txt
pip install -r requirements-dev.txt

REM Create .env if it doesn't exist
if not exist ".env" (
    echo Creating .env file...
    (
        echo # Backend Configuration
        echo DATABASE_URL=sqlite:///./pingchampions.db
        echo DEBUG=True
        echo CORS_ORIGINS=["http://localhost:5173"]
    ) > .env
    echo Note: Edit .env with your configuration
)

echo.
echo [OK] Backend setup complete
echo.

REM Frontend Setup
echo === Frontend Setup ===
echo.

cd ..\frontend

REM Check if Node.js is installed
where node >nul 2>nul
if %errorlevel% neq 0 (
    echo WARNING: Node.js is not installed
    echo Please install Node.js 18+ from https://nodejs.org/
) else (
    for /f "tokens=*" %%i in ('node -v') do set NODE_VERSION=%%i
    echo Node.js !NODE_VERSION! found
)

REM Install dependencies
if exist "node_modules" (
    echo Dependencies exist, running npm ci...
    call npm ci
) else (
    echo Installing frontend dependencies...
    call npm install
)

REM Create .env.local if it doesn't exist
if not exist ".env.local" (
    echo Creating .env.local file...
    (
        echo # Frontend Configuration
        echo VITE_API_BASE_URL=http://localhost:8000
        echo VITE_DEBUG=true
    ) > .env.local
    echo Note: Edit .env.local with your configuration
)

echo.
echo [OK] Frontend setup complete
echo.

REM Return to root
cd ..

REM Final setup
echo === Final Setup ===
echo.

REM Create directories if they don't exist
if not exist ".git\hooks" mkdir .git\hooks

echo.
echo ========================================
echo   [OK] Setup complete!
echo ========================================
echo.
echo Next steps:
echo.
echo 1. Start backend:
echo    cd backend
echo    venv\Scripts\activate
echo    uvicorn main:app --reload
echo.
echo 2. Start frontend (in another terminal):
echo    cd frontend
echo    npm run dev
echo.
echo 3. Read the guides:
echo    - TRUNK_BASED_DEV_GUIDE.md
echo    - COMMIT_CONVENTIONS.md
echo.
echo ========================================
echo.
