"""
Модуль конфігурації додатку.
Завантажує змінні оточення з файлу .env та формує шлях до бази даних SQLite.
Автоматично створює необхідні директорії для локальної БД.
"""

# app/core/config.py
import os

from dotenv import load_dotenv

load_dotenv()

BASE_DIR: str = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

DEFAULT_DB_PATH: str = f"sqlite:///{os.path.join(BASE_DIR, 'db', 'erp.db')}"

env_url: str | None = os.getenv("DATABASE_URL")
DATABASE_URL: str = env_url if env_url and env_url.strip() else DEFAULT_DB_PATH

if DATABASE_URL.startswith("sqlite:///"):
    clean_path: str = DATABASE_URL.replace("sqlite:///", "")
    db_dir: str = os.path.dirname(clean_path)
    if db_dir:
        os.makedirs(db_dir, exist_ok=True)