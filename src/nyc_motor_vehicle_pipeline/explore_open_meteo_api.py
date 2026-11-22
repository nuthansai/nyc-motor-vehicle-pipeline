import requests
import json
from config import OPEN_METEO_BASE_URL

params={
    "latitude": 18.2949307,
    "longitude": 83.8938844,
    "start_date": "2026-10-11",
    "end_date": "2026-11-12",
    "hourly": ["temperature_2m", "relative_humidity_2m"]
}

try:
    response = requests.get(
        OPEN_METEO_BASE_URL,
        params=params

    )

    data = response.json()

    with open("explore-open-meteo-api.json",'w') as f:
        json.dump(data, f, indent=4)
except Exception as e:
    print(e)