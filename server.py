from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import requests

app = FastAPI()

# Allow JS frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # adjust for production
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_URL = "https://globalmeteornetwork.org/data/traj_summary_data"


@app.get("/meteors")
def meteors(
    type: str = Query("latest", description="latest, yesterday, yearly"),
    date: str = Query(None, description="YYYY for yearly data")
):
    """
    Fetch meteors data from GMN summary files.

    type: "latest", "yesterday", "yearly"
    date: required for yearly, e.g., 2024
    """
    try:
        # Determine file URL
        if type == "latest":
            url = f"{BASE_URL}/traj_summary_latest_daily.txt"
        elif type == "yesterday":
            url = f"{BASE_URL}/traj_summary_yesterday.txt"
        elif type == "yearly" and date:
            url = f"{BASE_URL}/traj_summary_yearly_{date}.txt"
        else:
            return {"error": "Invalid parameters. Use type=latest|yesterday|yearly with optional date for yearly."}

        # Fetch file
        response = requests.get(url, timeout=15)
        if response.status_code != 200:
            return {"error": "File not found", "url": url, "status_code": response.status_code}

        lines = response.text.splitlines()
        # Skip comment lines starting with #
        data_lines = [l for l in lines if not l.startswith("#") and l.strip()]

        meteors = []

        for line in data_lines:
            parts = [p.strip() for p in line.split(";")]

            # Only take key columns, you can expand as needed
            try:
                meteors.append({
                    "id": parts[0],
                    "datetime": parts[2],
                    "vgeo": float(parts[15]) if parts[15] else None,
                    "lat_begin": float(parts[55]) if parts[55] else None,
                    "lon_begin": float(parts[57]) if parts[57] else None,
                    "ht_begin": float(parts[59]) if parts[59] else None,
                })
            except IndexError:
                continue  # skip malformed lines

        # Limit results for performance
        return {
            "count": len(meteors),
            "meteors": meteors[:1000]  # adjust or remove limit if safe
        }

    except Exception as e:
        return {"error": str(e)}
