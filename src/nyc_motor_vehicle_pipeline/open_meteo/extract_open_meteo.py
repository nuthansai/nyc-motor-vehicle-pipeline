import json
import requests
from nyc_motor_vehicle_pipeline.config import OPEN_METEO_BASE_URL, DATA_DIR

def download_nyc_boroughs():

    params = {
        "latitude": [40.7831, 40.6782, 40.7282, 40.8448, 40.5795],
        "longitude": [-73.9712, -73.9442, -73.7949, -73.8648, -74.1502],
        "start_date": "2025-10-01",
        "end_date": "2025-11-30",
        "hourly": ["temperature_2m", "rain", "snowfall", "precipitation", "wind_gusts_10m", "weather_code"]
    }
    try:
        weather_response = requests.get(OPEN_METEO_BASE_URL, params=params, timeout=10)

        weather_response.raise_for_status()

        data=weather_response.json()

        with open(f"{DATA_DIR}/weather_data.json", "w", encoding='utf-8') as f :
            json.dump(data, f, indent=4)

    except requests.Timeout as e:
        print(f"Timed out: {e}")
        raise

    except requests.ConnectionError as e:
        print(f"Network failed: {e}")
        raise

    except requests.exceptions.HTTPError as e:
        if weather_response.status_code == 401:
            print("failed due to unauthorized api key")
            raise
        elif weather_response.status_code == 403:
            print("Access forbidden. Stopping extraction.")
            raise
        elif weather_response.status_code == 429:
            print("API rate limit reached")
            raise

    except Exception as e:
        print(e)
        raise