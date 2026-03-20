from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from gmn_python_api import data_directory as dd
from gmn_python_api import meteor_trajectory_reader

app = FastAPI()

# Allow JS frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8080",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/meteors/{date}")
def meteors(date: str):
    try:
        if "-" in date:
            return {"error": "Use format YYYYMMDD (no dashes)"}

        # STEP 1: get raw data
        traj = dd.get_daily_file_content_by_date(date)

        if not traj:
            return {
                "step": "get_daily_file_content_by_date",
                "error": "No data returned",
                "date": date
            }

        # DEBUG: check type
        print("TRAJ TYPE:", type(traj))

        # STEP 2: parse data
        df = meteor_trajectory_reader.read_data(traj)

        if df is None:
            return {
                "step": "read_data",
                "error": "df is None"
            }

        if df.empty:
            return {
                "date": date,
                "count": 0,
                "meteors": []
            }

        return {
            "date": date,
            "count": len(df),
            "meteors": df.to_dict(orient="records")
        }

    except Exception as e:
        return {
            "step": "exception",
            "error": str(e)
        }
