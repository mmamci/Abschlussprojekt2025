import json, os, tempfile
from pathlib import Path
from typing import List

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

VARIABLES_FILE = DATA_DIR / "variables.json"
ENTRIES_FILE   = DATA_DIR / "entries.json"

def _ensure_file(path: Path):
    if not path.exists():
        path.write_text("[]", encoding="utf-8")

def _atomic_write(path: Path, data: List[dict]):
    tmp_fd, tmp_path = tempfile.mkstemp(dir=path.parent, text=True)
    with os.fdopen(tmp_fd, "w", encoding="utf-8") as tmp:
        json.dump(data, tmp, ensure_ascii=False, indent=2)
    os.replace(tmp_path, path)

# ---------- Variablen ----------
def load_variables():
    _ensure_file(VARIABLES_FILE)
    with open(VARIABLES_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_variables(vars_: list[dict]):
    _ensure_file(VARIABLES_FILE)
    _atomic_write(VARIABLES_FILE, vars_)

# ---------- Einträge ----------
def load_entries():
    _ensure_file(ENTRIES_FILE)
    with open(ENTRIES_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_entries(entries: list[dict]):
    _ensure_file(ENTRIES_FILE)
    _atomic_write(ENTRIES_FILE, entries)