import os

from dotenv import load_dotenv

load_dotenv()

class Settings:
	GREETING_MESSAGE: str = os.getenv("GREETING_MESSAGE", "Default Hello")
	ENVIRONMENT: str = os.getenv("ENVIRONMENT", "production")

settings = Settings()