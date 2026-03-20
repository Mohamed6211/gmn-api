from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import requests
import re
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

        for line in file_res.iter_lines(decode_unicode=True):
    if not line or line.startswith("#"):
        continue

    parts = [p.strip() for p in line.split(";")]

    if len(parts) < 70:
        continue

    try:
        meteors.append({
            "id": parts[0],
            "datetime": parts[2],

            "vgeo": float(parts[15]) if parts[15] else None,
            "elevation": float(parts[53]) if parts[53] else None,

            "lat_begin": float(parts[55]) if parts[55] else None,
            "lon_begin": float(parts[57]) if parts[57] else None,

            "lat_end": float(parts[61]) if parts[61] else None,
            "lon_end": float(parts[63]) if parts[63] else None,

            "duration": float(parts[67]) if parts[67] else None,
        })

        count += 1
        if count >= limit:
            break

    except:
        continue

        return {
            "count": count,
            "meteors": meteors
        }

    except Exception as e:
        return {"error": str(e)}

BASE_URL2 = "https://globalmeteornetwork.org/data/traj_summary_data/daily"
@app.get("/meteors-by-date/{date}")
def meteors_by_date(date: str, limit: int = 100):
    """
    date format: YYYYMMDD
    """
    try:
        # 1. Get directory listing HTML
        res = requests.get(BASE_URL2)
        if res.status_code != 200:
            return {"error": "Failed to access daily directory"}

        html = res.text

        # 2. Find matching filename using regex
        pattern = rf"traj_summary_{date}_solrange_[^\"']+\.txt"
        match = re.search(pattern, html)

        if not match:
            return {"error": f"No file found for date {date}"}

        filename = match.group(0)

        # 3. Build full file URL
        file_url = f"{BASE_URL2}/{filename}"

        # 4. Fetch the file
        file_res = requests.get(file_url, stream=True)
        if file_res.status_code != 200:
            return {"error": "Failed to fetch file"}

        meteors = []
        count = 0

        for line in file_res.iter_lines(decode_unicode=True):
            if not line or line.startswith("#"):
                continue

            parts = [p.strip() for p in line.split(";")]

            try:
                meteors.append({
                    "id": parts[0],
                    "datetime": parts[2],
                    "vgeo": float(parts[15]) if parts[15] else None,
                    "lat_begin": float(parts[55]) if parts[55] else None,
                    "lon_begin": float(parts[57]) if parts[57] else None,
                })

                count += 1
                if count >= limit:
                    break

            except:
                continue

        return {
            "date": date,
            "file": filename,
            "count": count,
            "meteors": meteors
        }

    except Exception as e:
        return {"error": str(e)}
