@echo off
echo ========================================
echo    অপরিচিতা RAG Chatbot - React App
echo ========================================
echo.

echo Starting FastAPI Backend...
start "Backend API" cmd /k "python api.py"

echo.
echo Waiting for backend to start...
timeout /t 5 /nobreak > nul

echo.
echo Starting React Frontend...
cd frontend
start "React Frontend" cmd /k "npm start"

echo.
echo ========================================
echo    Both servers are starting...
echo ========================================
echo Backend: http://localhost:8000
echo Frontend: http://localhost:3000
echo.
echo Press any key to exit this window...
pause > nul 