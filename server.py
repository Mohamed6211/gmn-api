from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from gmn_python_api import data_directory as dd

app = FastAPI()

# Allow requests from your frontend
origins = [
    "http://localhost:8080",  # your local frontend
    "https://your-production-frontend.com"  # optional, for production
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # or ["*"] to allow all origins (less secure)
    allow_credentials=True,
    allow_methods=["*"],     # GET, POST, PUT, DELETE, etc.
    allow_headers=["*"],     # headers like Content-Type, Authorization
)

# Your existing routes
@app.get("/meteors/{date}")
def get_meteors(date: str):
    # your existing code here
    return {"date": date, "data": []}
