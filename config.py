from dotenv import load_dotenv
import os

# Load variables from .env file
load_dotenv()

# Can get env variables via os.getenv
BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")
BASE_WEBSOCKET_URI = os.getenv("BASE_WEBSOCKET_URI", "ws://localhost:8000/ws")