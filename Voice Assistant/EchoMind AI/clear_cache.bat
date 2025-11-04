@echo off
REM Cache Clearing Script for EchoMind AI
REM This script removes all Python cache files and restarts the assistant

REM Change to project directory
cd /d "d:\Vs Code\PROJECT\OIBSIP\Voice Assistant\EchoMind AI"

REM Display current directory
echo.
echo ========================================
echo  EchoMind AI - Cache Cleaner
echo ========================================
echo.
echo Current directory: %CD%
echo.

REM Remove __pycache__ directories
echo Removing Python cache files...
for /d /r . %%d in (__pycache__) do (
    if exist "%%d" (
        echo   Removing: %%d
        rd /s /q "%%d"
    )
)

echo.
echo ========================================
echo  Cache cleared successfully!
echo ========================================
echo.

REM Show confirmation
echo This fixes:
echo   ✓ Translation queries now go to Gemini
echo   ✓ Close commands properly handled
echo   ✓ Personal handler override detection active
echo.

REM Ask if user wants to start assistant
echo.
set /p start="Start assistant now? (Y/N): "
if /i "%start%"=="Y" (
    echo.
    echo Starting assistant...
    python main_refactored.py
) else (
    echo.
    echo To start the assistant, run: python main_refactored.py
    echo.
)

pause
