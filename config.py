# config.py
from dotenv import load_dotenv
import os

# Загружаем переменные окружения из .env файла
load_dotenv()

# Теперь переменные можно получать через os.getenv
BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")
BASE_WEBSOCKET_URI = os.getenv("BASE_WEBSOCKET_URI", "ws://localhost:8000/ws")