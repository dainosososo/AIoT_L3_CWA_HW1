"""
SQLite Database ETL Engine (Gate 2)
Real CWA JSON -> ETL Pipeline -> SQLite (data.db).
Handles schema creation, deduplication via INSERT OR REPLACE, and query interfaces.
"""

import sqlite3
import os
import logging
from typing import List, Dict, Any

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

DB_PATH = os.path.join(os.path.dirname(__file__), "data.db")

def get_connection():
    """Returns a connection to SQLite database."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize SQLite database schema."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS weather_forecasts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                location_name TEXT NOT NULL,
                region TEXT NOT NULL,
                lat REAL NOT NULL,
                lon REAL NOT NULL,
                start_time TEXT NOT NULL,
                end_time TEXT NOT NULL,
                weather TEXT NOT NULL,
                min_temp REAL NOT NULL,
                max_temp REAL NOT NULL,
                avg_temp REAL NOT NULL,
                pop REAL NOT NULL,
                updated_at TEXT NOT NULL,
                UNIQUE(location_name, start_time)
            );
        """)
        conn.commit()
        logging.info("SQLite database schema initialized at data.db")

def save_forecasts(records: List[Dict[str, Any]]) -> int:
    """ETL Pipeline: Insert or replace forecast records into SQLite."""
    init_db()
    inserted_count = 0
    with get_connection() as conn:
        cursor = conn.cursor()
        for r in records:
            cursor.execute("""
                INSERT OR REPLACE INTO weather_forecasts (
                    location_name, region, lat, lon, start_time, end_time,
                    weather, min_temp, max_temp, avg_temp, pop, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
            """, (
                r["location_name"], r["region"], r["lat"], r["lon"],
                r["start_time"], r["end_time"], r["weather"],
                r["min_temp"], r["max_temp"], r["avg_temp"], r["pop"], r["updated_at"]
            ))
            inserted_count += 1
        conn.commit()
    logging.info(f"ETL completed: Processed & saved {inserted_count} records to SQLite.")
    return inserted_count

def get_all_forecasts() -> List[Dict[str, Any]]:
    """Retrieve all latest location forecasts from SQLite."""
    init_db()
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM weather_forecasts ORDER BY region, location_name;")
        rows = cursor.fetchall()
        return [dict(row) for row in rows]

def get_forecasts_by_region(region: str) -> List[Dict[str, Any]]:
    """Retrieve forecasts for a specific region from SQLite."""
    init_db()
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM weather_forecasts WHERE region = ? ORDER BY location_name;", (region,))
        rows = cursor.fetchall()
        return [dict(row) for row in rows]

if __name__ == "__main__":
    from cwa_api import fetch_cwa_forecast
    records = fetch_cwa_forecast()
    save_forecasts(records)
    all_data = get_all_forecasts()
    print(f"Gate 2 ETL Verification: Successfully queried {len(all_data)} records from SQLite.")
