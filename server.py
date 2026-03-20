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
        traj = dd.get_daily_file_content_by_date(date)

        if not traj:
            return {
                "date": date,
                "count": 0,
                "meteors": [],
                "message": "No trajectory data found"
            }

        df = meteor_trajectory_reader.read_data(traj)

        if df is None or df.empty:
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
            "date": date,
            "error": str(e)
        }
