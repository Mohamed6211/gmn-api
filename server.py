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
    type: str = "latest",
    date: str = None,
    limit: int = 100  # 👈 important
):
    try:
        if type == "latest":
            url = f"{BASE_URL}/daily/traj_summary_latest_daily.txt"

        elif type == "yesterday":
            url = f"{BASE_URL}/daily/traj_summary_yesterday.txt"

        elif type == "yearly" and date:
            url = f"{BASE_URL}/traj_summary_yearly_{date}.txt"

        else:
            return {"error": "Invalid parameters"}

        response = requests.get(url, stream=True)

        if response.status_code != 200:
            return {"error": "File not found"}

        meteors = []
        count = 0

        for line in response.iter_lines(decode_unicode=True):
            if not line or line.startswith("#"):
                continue

            parts = [p.strip() for p in line.split(";")]

            try:
                meteors.append({
                    "id": parts[0],
                    "datetime": parts[2],
                    "vgeo": float(parts[15]) if parts[15] else None,
                })
                count += 1

                if count >= limit:  # 👈 STOP EARLY
                    break

            except:
                continue

        return {
            "count": count,
            "meteors": meteors
        }

    except Exception as e:
        return {"error": str(e)}
