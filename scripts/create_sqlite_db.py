import sqlite3
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

DB_PATH = BASE_DIR / "db.sqlite3"


connection = sqlite3.connect(DB_PATH)
