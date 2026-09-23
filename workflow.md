# Workflow & System Architecture: Taiwan Weather Forecast & Temperature Visualization

> **Project**: AIoT Level 3 Homework 1 (`AIoT_L3_CWA_HW1`)  
> **Data Source**: [CWA OpenData Platform](https://opendata.cwa.gov.tw/index)  
> **Reference**: 24-Step AI Innovation Micro-Course Roadmap (AI 創新微課程 - 台灣天氣預報應用)

---

## 1. System Architecture Diagram (Mermaid)

```mermaid
flowchart TD
    subgraph Phase 1: Data Ingestion & Storage
        A[CWA OpenData Platform<br/>opendata.cwa.gov.tw] -->|1. Requests JSON| B[Python CWA API Ingestion Engine]
        B -->|2. Extract MinT / MaxT / Wx| C[Pandas Data Cleaning & Normalization]
        C -->|3. Insert / Update| D[(SQLite Database<br/>data.db)]
    end

    subgraph Phase 2: Web App & Temperature Chart
        D -->|4. SQL Query| E[Streamlit Weather Dashboard Engine]
        E --> F[Region Selector Dropdown<br/>北部 / 中部 / 南部 / 東部 / 離島]
        E --> G[📈 Temperature Line Chart<br/>MaxT vs MinT Daily Trend]
        E --> H[📋 Weekly Forecast Table<br/>Date, MinT, MaxT, Wx]
    end

    subgraph Phase 3: Taiwan Map Visualization
        E --> I[🗺️ Taiwan Interactive Weather Map<br/>Folium / Leaflet / Windy]
        I --> J[Color Scale Markers<br/>🔵 <20°C | 🟢 20-25°C | 🟡 25-30°C | 🔴 >30°C]
    end

    subgraph Phase 4: GitHub Deployment
        E --> K[Octocat GitHub Synchronization<br/>AIoT_L3_CWA_HW1 Repository]
    end
```

---

## 2. Text & Pipeline Architecture Overview

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                 TAIWAN WEATHER APPLICATION END-TO-END PIPELINE              │
└─────────────────────────────────────────────────────────────────────────────┘
  [Phase A: API & Data]      [Phase B: Web UI & Chart]   [Phase C: Map & GitHub]
 ┌────────────────────────┐  ┌────────────────────────┐  ┌─────────────────────┐
 │ • Fetch CWA JSON       │  │ • Streamlit Dashboard  │  │ • Folium Map        │
 │ • Clean with Pandas    │─>│ • Region Dropdown      │─>│ • Temp Color Scale  │
 │ • Store in SQLite DB   │  │ • MaxT / MinT Line    │  │ • Date Picker       │
 │ • SQL Query Layer      │  │ • Weekly Data Table    │  │ • Push to GitHub    │
 └────────────────────────┘  └────────────────────────┘  └─────────────────────┘
```

---

## 3. 24-Step Micro-Course Roadmap Integration

The system directly implements the 24-step micro-course learning roadmap:

```text
┌───────────────────────────────────────────────────────────────────────────────┐
│ 1. 課程介紹        2. 天氣與生活        3. CWA OpenData    4. API 資料取得(JSON)  │
│ 5. JSON 結構解析   6. 最高/最低溫提取   7. Pandas 資料整理 8. 建立 SQLite 資料庫  │
│ 9. 資料庫 Schema   10. SQL 查詢驗證     11. Streamlit/Web  12. SQL 資料讀取      │
│ 13. 地區選單互動   14. 繪製折線圖       15. 資料表格呈現   16. Web App 介面整合   │
│ 17. 地圖視覺化     18. 互動式天氣地圖   19. 完整成果展示   20. 程式碼優化        │
│ 21. GitHub 版本控制 22. 延伸應用與 AI   23. 重點整理       24. 未來探索          │
└───────────────────────────────────────────────────────────────────────────────┘
```

---

## 4. Phase-by-Phase Detailed Workflow

### Phase A: Data Ingestion & Storage (Steps 1–10)
1. **API Acquisition**: Use Python `requests` / `httpx` to retrieve weather forecast JSON datasets (`F-C0032-001` 36-hour / 7-day forecast) and observation feeds from `opendata.cwa.gov.tw`.
2. **JSON Structure Parsing**: Parse location arrays (`locationName`), weather elements (`MinT` minimum temperature, `MaxT` maximum temperature, `Wx` weather phenomenon), and time intervals.
3. **Data Transformation with Pandas**: Clean invalid values, structure fields, and aggregate statistics across Taiwan regions (`北部地區`, `中部地區`, `南部地區`, `東部地區`, `離島地區`).
4. **SQLite Storage (`data.db`)**: Store cleaned regional forecast records into a local SQLite database (`TemperatureForecasts` table).
5. **SQL Query Engine**: Validate data integrity via SQL queries to prevent duplicate insertions and ensure fresh dataset updates.

---

### Phase B: Interactive Web App & Temperature Line Chart (Steps 11–16)
6. **Streamlit App Setup**: Initialize the web application frontend (`app.py`).
7. **Region Selector**: Interactive dropdown menu allowing users to select regional views (`北部地區`, `中部地區`, etc.).
8. **Temperature Line Graph (📈 折線圖)**:
   - **X-Axis**: Forecast dates (e.g., `04/14`, `04/15`, `04/16`...)
   - **Y-Axis**: Temperature in Celsius (°C)
   - **Dual-Line Display**: **MaxT** (Red curve for daily maximum) vs. **MinT** (Blue curve for daily minimum).
9. **Weekly Forecast Table (📋 資料表格)**: A clean tabular overview displaying Date, MinT, MaxT, and weather conditions.

---

### Phase C: Taiwan Weather Map Visualization (Steps 17–20)
10. **Interactive Taiwan Weather Map (🗺️ 地圖視覺化)**: Render an interactive map of Taiwan using `Folium` / `Leaflet` / `Windy API`.
11. **Temperature Color Legend**:
    - `< 20°C` 🔵 **Cold** (Blue)
    - `20 – 25°C` 🟢 **Comfortable** (Green)
    - `25 – 30°C` 🟡 **Warm** (Yellow)
    - `> 30°C` 🔴 **Hot** (Red)
12. **Date Picker Filter**: Interactive date controls allowing users to view map temperature distributions across different days.
13. **Unified Dashboard**: Combine region selector, line graph, weather table, and interactive map into a single cohesive interface.

---

### Phase D: GitHub Deployment & Extension (Steps 21–24)
14. **GitHub Synchronization**: Commit and push all modular source code (`app.py`, `cwa_api.py`, `database.py`, `charts.py`, `map_viz.py`, `README.md`, `workflow.md`) to GitHub repository [https://github.com/dainosososo/AIoT_L3_CWA_HW1.git](https://github.com/dainosososo/AIoT_L3_CWA_HW1.git).
15. **Future AI Extensions**: Integration with Line Bot alerts, disaster prevention warnings, and AI-driven weather insights.

---

## 5. File Structure

```text
AIoT_L3_CWA_HW1/
├── README.md                   # Project overview & design specification
├── workflow.md                 # Detailed workflow & architecture (this file)
├── requirements.txt            # Python dependencies (Streamlit, Folium, Pandas, Requests, etc.)
├── .env.example                # CWA OpenData API Key configuration template
├── app.py                      # Streamlit Main Web Dashboard
├── cwa_api.py                  # CWA OpenData Fetching & Ingestion Service
├── database.py                 # SQLite DB Setup & Query Utilities
├── charts.py                   # MaxT / MinT Line Chart Generators
└── map_viz.py                  # Folium / Leaflet Taiwan Weather Map Engine
```
