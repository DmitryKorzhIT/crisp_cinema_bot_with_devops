import os
from dotenv import load_dotenv

load_dotenv()

# Telegram Bot Token.
APP_BOT_TOKEN = os.getenv("APP_BOT_TOKEN")

# PostgreSQL database data.
DB_DBNAME = os.getenv("DB_DBNAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
