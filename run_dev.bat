@echo off
echo ========================================================
echo Starting Development Servers for "This is business"
echo ========================================================
echo.
echo 1. Starting Backend API on http://127.0.0.1:8000 ...
start "TIB Backend" cmd /k "python backend\main.py"
echo 2. Starting Frontend Dev Server on http://localhost:5173 ...
cd frontend
npm run dev
pause
