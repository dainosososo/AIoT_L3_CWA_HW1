"""
Local & LAN Server Runner for Taiwan Weather GIS Dashboard
Reads data directly from SQLite (data.db), triggers real-time scraper updates,
and serves the Taiwan GIS Web Dashboard on http://0.0.0.0:8000 (accessible across LAN PCs)
"""

import os
import uvicorn
from app import app

if __name__ == "__main__":
    print("Starting Taiwan Weather GIS Web Server on http://0.0.0.0:8000 (Accessible from localhost & LAN PCs) ...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
