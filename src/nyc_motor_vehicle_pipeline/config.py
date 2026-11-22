import os
from dotenv import load_dotenv

load_dotenv()

MVC_APP_TOKEN = os.getenv("MVC_APP_TOKEN")

MVC_BASE_URL = "https://data.cityofnewyork.us/api/v3/views/h9gi-nx95/query.json"

OPEN_METEO_BASE_URL = "https://archive-api.open-meteo.com/v1/archive"