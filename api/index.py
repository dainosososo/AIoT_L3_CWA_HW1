from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import os

from database import get_all_forecasts, get_forecasts_by_region, save_forecasts
from cwa_scraper import scrape_cwa_web_platform

app = FastAPI(
    title="Public Taiwan Weather GIS Dashboard",
    description="Taiwan Weather Visualization API based on CWA OpenData and SQLite",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_event():
    records = scrape_cwa_web_platform()
    save_forecasts(records)

@app.get("/api/health")
def health_check():
    return {
        "status": "ok",
        "service": "Taiwan Weather GIS Dashboard",
        "database": "SQLite /tmp/data.db connected"
    }

@app.get("/api/gis/locations")
def get_gis_locations(region: str = None):
    if region and region != "全臺地區":
        locations = get_forecasts_by_region(region)
    else:
        locations = get_all_forecasts()
    return {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [loc["lon"], loc["lat"]]
                },
                "properties": {
                    "location_name": loc["location_name"],
                    "region": loc["region"],
                    "weather": loc["weather"],
                    "min_temp": loc["min_temp"],
                    "max_temp": loc["max_temp"],
                    "avg_temp": loc["avg_temp"],
                    "pop": loc["pop"],
                    "start_time": loc["start_time"],
                    "updated_at": loc["updated_at"]
                }
            }
            for loc in locations
        ]
    }

@app.get("/api/gis/refresh")
def refresh_data():
    records = scrape_cwa_web_platform()
    count = save_forecasts(records)
    return {"status": "success", "updated_count": count}

@app.get("/", response_class=HTMLResponse)
def read_root():
    static_file = os.path.join(os.path.dirname(__file__), "..", "static", "index.html")
    if os.path.exists(static_file):
        with open(static_file, "r", encoding="utf-8") as f:
            return f.read()
    return "<h1>Public Taiwan Weather GIS Dashboard Serverless</h1>"
