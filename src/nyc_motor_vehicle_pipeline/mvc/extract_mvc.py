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
        mvc_response = requests.get(MVC_BASE_URL, params=params, headers=headers, timeout=10) # type: ignore

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
        status_code = e.response.status_code if e.response is not None else None
        if status_code == 401:
            print("failed due to unauthorized api key")
            raise
        elif status_code == 403:
            print("Access forbidden. Stopping extraction.")
            raise
        elif status_code == 429:
            print("API rate limit reached")
            raise

    except Exception as e:
        print(e)
        raise