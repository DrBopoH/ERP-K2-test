import os

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

DEFAULT_DB_PATH = f"sqlite:///{os.path.join(BASE_DIR, 'db', 'erp.db')}"

DATABASE_URL = os.getenv("DATABASE_URL", DEFAULT_DB_PATH)

if DATABASE_URL.startswith("sqlite:///"):
	clean_path = DATABASE_URL.replace("sqlite:///", "")
	db_dir = os.path.dirname(clean_path)
	if db_dir:
		os.makedirs(db_dir, exist_ok=True)