from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from gmn_python_api import data_directory as dd
from gmn_python_api import meteor_trajectory_reader

app = FastAPI()

# Allow JS frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/meteors/{date}")
def get_meteors(date: str):

    try:
        # Download GMN trajectory file for the date
        traj_file_content = dd.get_daily_file_content_by_date(date)

        # Convert to pandas dataframe
        traj_df = meteor_trajectory_reader.read_data(traj_file_content)

        meteors = []

        for _, row in traj_df.iterrows():

            meteors.append({
                "time": str(row["UTC Time"]),
                "v_geo_km_s": float(row["Vgeo (km/s)"]),
                "ra": float(row["RAgeo (deg)"]),
                "dec": float(row["DECgeo (deg)"]),
                "iau_code": str(row["IAU (code)"]),
                "stations": str(row["stations"])
            })

        return {
            "date": date,
            "count": len(meteors),
            "meteors": meteors
        }

    except Exception as e:
        return {
            "date": date,
            "error": str(e),
            "meteors": []
        }
