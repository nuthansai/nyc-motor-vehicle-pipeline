import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

MVC_APP_TOKEN = os.getenv("MVC_APP_TOKEN")

MVC_BASE_URL = "https://data.cityofnewyork.us/api/v3/views/h9gi-nx95/query.json"

OPEN_METEO_BASE_URL = "https://archive-api.open-meteo.com/v1/archive"

PROJECT_ROOT = Path(__file__).parent.parent.parent

DATA_DIR = PROJECT_ROOT / 'data'

DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
DB_PORT = os.getenv("DB_PORT")
