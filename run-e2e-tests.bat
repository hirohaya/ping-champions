@echo off
REM Playwright E2E Test Runner for Ping Champions

setlocal enabledelayedexpansion

echo ========================================
echo Ping Champions - E2E Test Runner
echo ========================================
echo.

echo Starting backend...
start "" python run_backend.py

REM Wait for backend to start
timeout /t 5 /nobreak

echo Starting frontend...
cd frontend
start "" npm run dev

REM Wait for frontend to start
cd ..
timeout /t 10 /nobreak

echo.
echo Running Playwright tests...
cd frontend

set SKIP_SERVER=1
call npm run e2e:serial

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================
    echo SUCCESS: All tests completed!
    echo ========================================
    exit /b 0
) else (
    echo.
    echo ========================================
    echo FAILED: Tests did not pass
    echo ========================================
    exit /b 1
)
