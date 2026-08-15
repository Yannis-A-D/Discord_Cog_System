"""Run helper for the bot (cross-platform).

Behavior:
- Prefer a project virtualenv located at `.venv/` then `venv/` then `env/`.
- If necessary dependencies are missing, install them into the chosen Python interpreter
  using `-m pip install -r requirements.txt`.
- Finally, run `src/bot.py` using that interpreter.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path
import shutil

ROOT = Path(__file__).parent
REQS = ROOT / "requirements.txt"

# Candidate venv paths
venv_candidates = [ROOT / '.venv', ROOT / 'venv', ROOT / 'env']

def find_python_in_venv(venv_path: Path) -> Path | None:
    if sys.platform == 'win32':
        py = venv_path / 'Scripts' / 'python.exe'
    else:
        py = venv_path / 'bin' / 'python'
    return py if py.exists() else None

def choose_python() -> Path:
    for v in venv_candidates:
        py = find_python_in_venv(v)
        if py:
            print(f"Using virtualenv Python at: {py}")
            return py

    sysp = shutil.which('python') or shutil.which('python3')
    if sysp:
        print(f"No project venv found; using system Python at: {sysp}")
        return Path(sysp)

    raise SystemExit("No usable Python interpreter found on PATH.")

def run(cmd: list[str], check: bool = True):
    print(f"Running: {' '.join(cmd)}")
    res = subprocess.run(cmd)
    if check and res.returncode != 0:
        raise SystemExit(res.returncode)
    return res.returncode

def main():
    python = choose_python()

    # Check if discord is importable in the chosen interpreter
    check_cmd = [str(python), '-c', 'import discord']
    ok = subprocess.run(check_cmd)
    if ok.returncode != 0:
        if not REQS.exists():
            raise SystemExit("Dependencies missing and requirements.txt not found.")
        print("Installing dependencies into the chosen interpreter...")
        run([str(python), '-m', 'pip', 'install', '-r', str(REQS)])

    # Now run the bot
    run([str(python), str(ROOT / 'src' / 'bot.py')], check=True)

if __name__ == '__main__':
    main()
