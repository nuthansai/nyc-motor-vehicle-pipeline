import json
import requests
from nyc_motor_vehicle_pipeline.config import MVC_APP_TOKEN, MVC_BASE_URL,DATA_DIR


def download_mvc():

    params={
        "query": "SELECT * WHERE crash_date >= '2025-10-01T00:00:00.000' AND crash_date < '2025-11-30T23:59:59.000'",
    }

    headers={
        "X-App-Token": MVC_APP_TOKEN
    }

    try:
        mvc_response = requests.get(MVC_BASE_URL, params=params, headers=headers, timeout=10)

        mvc_response.raise_for_status()

        data=mvc_response.json()

        with open(f"{DATA_DIR}/mvc_crashes_data.json", "w", encoding='utf-8') as f :
            json.dump(data, f, indent=4)


    except requests.Timeout as e:
        print(f"Timed out: {e}")
        raise

    except requests.ConnectionError as e:
        print(f"Network failed: {e}")
        raise

    except requests.exceptions.HTTPError as e:
        if mvc_response.status_code == 401:
            print("failed due to unauthorized api key")
            raise
        elif mvc_response.status_code == 403:
            print("Access forbidden. Stopping extraction.")
            raise
        elif mvc_response.status_code == 429:
            print("API rate limit reached")
            raise

    except Exception as e:
        print(e)
        raise