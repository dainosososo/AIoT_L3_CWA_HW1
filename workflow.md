# Workflow & System Architecture: Taiwan Weather Forecast & Temperature Visualization

> **Project**: AIoT Level 3 Homework 1 (`AIoT_L3_CWA_HW1`)  
> **Data Source**: [CWA OpenData Platform](https://opendata.cwa.gov.tw/index)  
> **Reference**: 24-Step AI Innovation Micro-Course Roadmap (AI 創新微課程 - 台灣天氣預報應用) & 5 Milestone Gates

![AI Coding Agent Workflow - Courage the Cowardly Dog](static/courage_ai_coding_workflow.jpg)

---

## 1. System Architecture Diagram (Mermaid)

```mermaid
flowchart TD
    subgraph Phase 1: Data Ingestion & Storage (Gates 1 & 2)
        A[CWA OpenData Platform<br/>opendata.cwa.gov.tw] -->|1. Requests JSON| B[Python CWA API Ingestion Engine<br/>cwa_api.py]
        B -->|2. Extract MinT / MaxT / Wx| C[Pandas Data Cleaning & Normalization]
        C -->|3. ETL Insert / Replace| D[(SQLite Database<br/>data.db / database.py)]
    end

    subgraph Phase 2: Web App & Temperature Chart (Gate 3)
        D -->|4. SQL Query| E[FastAPI / Streamlit Engine<br/>app.py]
        E --> F[Region Selector Dropdown<br/>北部 / 中部 / 南部 / 東部 / 離島]
        E --> G[📈 Temperature Line Chart<br/>MaxT vs MinT Daily Trend]
        E --> H[📋 Weekly Forecast Table<br/>Date, MinT, MaxT, Wx]
    end

    subgraph Phase 3: Taiwan Map Visualization (Gate 3)
        E --> I[🗺️ Taiwan Interactive Weather Map<br/>Leaflet / OpenStreetMap / GeoJSON]
        I --> J[Color Scale Markers<br/>🔵 <20°C | 🟢 20-25°C | 🟡 25-30°C | 🔴 >30°C]
    end

    subgraph Phase 4: Security & Deployment (Gates 4 & 5)
        E --> K[Octocat GitHub Synchronization<br/>AIoT_L3_CWA_HW1 Repository]
        K --> L[Vercel Serverless Auto-Deploy<br/>vercel.json]
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
 │ • Fetch CWA JSON       │  │ • Streamlit Dashboard  │  │ • Leaflet GIS Map   │
 │ • Clean with Pandas    │─>│ • Region Dropdown      │─>│ • Temp Color Scale  │
 │ • Store in SQLite DB   │  │ • MaxT / MinT Line    │  │ • Date Picker       │
 │ • SQL Query Layer      │  │ • Weekly Data Table    │  │ • Push to GitHub    │
 └────────────────────────┘  └────────────────────────┘  └─────────────────────┘
```

---

## 3. 五大驗收關卡實作細節 (5 Milestone Gates Implementation)

| 關卡 (Gate) | 要做什麼 (Action) | 驗收重點 (Acceptance Criteria) | 實作檔案 (Files) |
| :--- | :--- | :--- | :--- |
| **1. CWA API** | 用 API Key 取得真實 CWA Forecast JSON (`F-C0032-001`) | HTTP 成功，取得 Location、Time、Weather (`Wx`)、MinT、MaxT、PoP (降雨機率)。包含離線備用生成器。 | [cwa_api.py](file:///C:/Users/user/.gemini/antigravity/scratch/AIoT_L3_CWA_HW1/cwa_api.py) |
| **2. Database** | 真實 JSON -> ETL Pipeline -> SQLite | SQL 可以正確查到各地區天氣資料，完成 `INSERT OR REPLACE` 重複資料處理。 | [database.py](file:///C:/Users/user/.gemini/antigravity/scratch/AIoT_L3_CWA_HW1/database.py) |
| **3. Taiwan GIS** | SQLite -> Web -> Taiwan Map (7 個小步驟) | Leaflet + OpenStreetMap + GeoJSON，地圖上的天氣資料必須直接來自 SQLite DB。 | [app.py](file:///C:/Users/user/.gemini/antigravity/scratch/AIoT_L3_CWA_HW1/app.py)<br/>[static/index.html](file:///C:/Users/user/.gemini/antigravity/scratch/AIoT_L3_CWA_HW1/static/index.html) |
| **4. GitHub** | 整理並 Push 完整專案到 GitHub | README/workflow 完整，配置 `.gitignore` 確保 `.env` API Key 與 Secret 絕對不可上傳。 | [.gitignore](file:///C:/Users/user/.gemini/antigravity/scratch/AIoT_L3_CWA_HW1/.gitignore)<br/>[.env.example](file:///C:/Users/user/.gemini/antigravity/scratch/AIoT_L3_CWA_HW1/.env.example) |
| **5. Vercel** | GitHub -> Vercel 自動部署 | Public URL 運作正常，GitHub Push 可自動觸發 Vercel Auto Deploy。 | [vercel.json](file:///C:/Users/user/.gemini/antigravity/scratch/AIoT_L3_CWA_HW1/vercel.json) |

### 🔍 Gate 3 的 7 個小步驟 (Gate 3 Sub-steps)

```text
3A: Taiwan Map 初始化 ─> 3B: One Location Marker ─> 3C: Weather Popup ─> 3D: Taiwan Locations (22 縣市)
                                                                                  │
3G: Full GIS Dashboard ◄─ 3F: Taiwan GeoJSON ◄─ 3E: Database -> GIS API ◄─────────┘
(選單過濾/折線圖/圖例)
```

1. **3A Taiwan Map**： Leaflet 暗色系質感地圖初始化，定位於台灣中心 (`23.7°N, 120.95°E`)。
2. **3B One Location Marker**：根據氣溫動態標註彩色圓點 (🔵 <20°C, 🟢 20-25°C, 🟡 25-30°C, 🔴 >30°C)。
3. **3C Weather Popup**：點擊 Marker 顯示地點、即時氣溫、天氣現象、最低/最高溫與降雨機率。
4. **3D Taiwan Locations**：涵蓋全台灣 22 縣市地理座標與氣象監測站點。
5. **3E Database -> GIS**：透過 FastAPI `/api/gis/locations` 直接綁定 SQLite `data.db` 數據。
6. **3F Taiwan GeoJSON**：提供標準 GeoJSON FeatureCollection 格式接口。
7. **3G Full GIS Dashboard**：整合地區選單過濾 (全臺/北部/中部/南部/東部/離島)、統計面板、氣溫圖例與 Chart.js MaxT/MinT 折線圖。

---

## 4. 24-Step Micro-Course Roadmap Integration

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

## 5. File Structure

```text
AIoT_L3_CWA_HW1/
├── README.md                   # Project overview & design specification
├── workflow.md                 # Detailed workflow, 5 Gates & architecture (this file)
├── requirements.txt            # Python dependencies (FastAPI, Uvicorn, Pandas, Requests, etc.)
├── .env.example                # CWA OpenData API Key configuration template
├── .gitignore                  # Git secret protection
├── app.py                      # FastAPI Main Web & GIS API Server (Gate 3)
├── cwa_api.py                  # CWA OpenData Ingestion & Fallback Engine (Gate 1)
├── database.py                 # SQLite DB Setup & ETL Deduplication (Gate 2)
├── vercel.json                 # Vercel Serverless Auto-Deployment Config (Gate 5)
└── static/
    └── index.html              # Leaflet GIS Map & Chart.js Dashboard (Gate 3)
```
