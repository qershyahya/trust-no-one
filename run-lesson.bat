@echo off
rem  Double-click this to start the lesson.
cd /d "%~dp0"

where py >nul 2>nul && (set PY=py) || (set PY=python)

%PY% -c "import pygame" >nul 2>nul
if errorlevel 1 (
    echo Installing pygame, one moment...
    %PY% -m pip install pygame
    if errorlevel 1 (
        echo.
        echo Could not install pygame. Try typing this yourself:
        echo     py -m pip install pygame
        echo.
        pause
        exit /b 1
    )
)

echo Starting the lesson. Your browser will open in a moment.
echo Close this window, or press Ctrl+C in it, to stop.
echo.
%PY% main.py
pause
