@echo off
setlocal
if exist "%~dp0.venv\Scripts\python.exe" (
  echo Using .venv Python
  "%~dp0.venv\Scripts\python.exe" -m pip install -r "%~dp0requirements.txt"
  "%~dp0.venv\Scripts\python.exe" "%~dp0src\bot.py"
) else (
  echo No .venv found — using system python. You can create a venv with: python -m venv .venv
  python -m pip install -r "%~dp0requirements.txt"
  python "%~dp0src\bot.py"
)
endlocal
