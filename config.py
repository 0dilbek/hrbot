from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
ADMINS = list(map(int, os.getenv("ADMINS").split(",")))
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
BOT_API_SERVER = os.getenv("BOT_API_SERVER", "https://api.telegram.org")
WEBHOOK_BASE_URL = os.getenv("WEBHOOK_BASE_URL", "http://localhost:8080")
WEBHOOK_PATH = os.getenv("WEBHOOK_PATH", "/webhook")
WEBHOOK_LISTEN_HOST = os.getenv("WEBHOOK_LISTEN_HOST", "0.0.0.0")
WEBHOOK_LISTEN_PORT = int(os.getenv("WEBHOOK_LISTEN_PORT", 8080))