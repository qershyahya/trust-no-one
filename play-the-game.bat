@echo off
rem  Double-click this to play the finished game.
cd /d "%~dp0"
where py >nul 2>nul && (set PY=py) || (set PY=python)
%PY% steps\step57.py
if errorlevel 1 pause
