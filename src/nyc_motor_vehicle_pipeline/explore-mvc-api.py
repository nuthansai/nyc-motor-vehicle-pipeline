import json
import requests
from config import MVC_BASE_URL, MVC_APP_TOKEN

params= {
    "query": "SELECT * WHERE crash_date >= '2026-09-01T00:00:00.000' AND crash_date < '2026-10-02T00:00:00.000'",
    "pageNumber": 1,
    "pageSize": 500
}

headers = {"X-App-Token": MVC_APP_TOKEN}

try:
    response = requests.get(
        MVC_BASE_URL,
        params=params,
        headers=headers
    )

    print(response.status_code)

    data = response.json()

    with open("explore-mvc-api.json",'w') as f:
        json.dump(data, f, indent=4)
except Exception as e:
    print(e)
