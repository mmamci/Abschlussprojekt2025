import json
from pathlib import Path
from typing import Any, List

# Basisordner
DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)                 # Ordner sicher anlegen

# Pfade
VARIABLES_FILE = DATA_DIR / "variables.json"
ENTRIES_FILE   = DATA_DIR / "entries.json"


def _ensure_file(path: Path) -> None:
    """
    Stellt sicher, dass die Datei existiert.
    Wenn nicht, wird sie mit einer leeren JSON-Liste '[]' angelegt.
    """
    if not path.exists():
        try:
            path.write_text("[]", encoding="utf-8")
        except PermissionError as e:
            raise PermissionError(
                f"Kein Schreibzugriff auf '{path}'. "
                "Bitte prüfe Rechte oder schließe Programme, die die Datei geöffnet haben."
            ) from e


# ---------- Variablen ----------
def load_variables() -> List[dict]:
    _ensure_file(VARIABLES_FILE)
    try:
        return json.loads(VARIABLES_FILE.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return []


def save_variables(variables: List[dict]) -> None:
    _ensure_file(VARIABLES_FILE)
    try:
        VARIABLES_FILE.write_text(
            json.dumps(variables, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
    except PermissionError as e:
        raise PermissionError(
            f"Fehler beim Schreiben in '{VARIABLES_FILE}'. "
            "Ist die Datei geöffnet oder schreibgeschützt?"
        ) from e


# ---------- Einträge ----------
def load_entries() -> List[dict]:
    _ensure_file(ENTRIES_FILE)
    try:
        return json.loads(ENTRIES_FILE.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return []


def save_entries(entries: List[dict]) -> None:
    _ensure_file(ENTRIES_FILE)
    try:
        ENTRIES_FILE.write_text(
            json.dumps(entries, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
    except PermissionError as e:
        raise PermissionError(
            f"Fehler beim Schreiben in '{ENTRIES_FILE}'. "
            "Ist die Datei geöffnet oder schreibgeschützt?"
        ) from e
    