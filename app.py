"""
FastAPI Server & GIS Web Endpoint (Gate 3)
Serves SQLite DB records to Leaflet GIS Web App.
Includes GeoJSON support, health checks, and static file serving.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import logging

from database import get_all_forecasts, get_forecasts_by_region, save_forecasts
from cwa_api import fetch_cwa_forecast

logging.basicConfig(level=logging.INFO)

app = FastAPI(
    title="Public Taiwan Weather GIS Dashboard",
    description="Taiwan Weather Visualization API based on CWA OpenData and SQLite",
    version="1.0.0"
)

# Enable CORS for frontend flexibility
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize DB on startup
@app.on_event("startup")
def startup_event():
    records = fetch_cwa_forecast()
    save_forecasts(records)
    logging.info("Startup complete: Initialized CWA Weather Database.")

@app.get("/api/health")
def health_check():
    """Gate 3 / Gate 5 Health Endpoint."""
    return {
        "status": "ok",
        "service": "Taiwan Weather GIS Dashboard",
        "database": "SQLite data.db connected"
    }

@app.get("/api/forecast/latest")
def get_latest_forecast():
    """Returns latest forecasts directly from SQLite DB."""
    data = get_all_forecasts()
    return {
        "source": "CWA OpenData / SQLite",
        "count": len(data),
        "locations": data
    }

@app.get("/api/gis/locations")
def get_gis_locations(region: str = None):
    """Gate 3E: Database -> GIS JSON Endpoint for Leaflet Map."""
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
    """Trigger manual fetch from CWA and update SQLite."""
    records = fetch_cwa_forecast()
    count = save_forecasts(records)
    return {"status": "success", "updated_count": count}

# Mount static files directory if exists
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/")
def read_root():
    index_path = os.path.join(static_dir, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "Public Taiwan Weather GIS API is running. Visit /api/gis/locations for GIS data."}
