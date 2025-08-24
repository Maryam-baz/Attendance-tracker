@echo off
REM --------------------------------------
REM Start Python backend
REM --------------------------------------
echo Starting Python backend...
start "" cmd /k "python backend\app.py"

REM Wait a few seconds to let the server start
timeout /t 5

REM --------------------------------------
REM Compile and run Java frontend
REM --------------------------------------
echo Running Java frontend...
cd frontend
javac Frontend\Main.java
java Frontend.Main

pause
cd ..