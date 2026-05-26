---
description: 
alwaysApply: true
---

# Web Log Anomaly Detector — Project Context

**Purpose:** Full-stack web application to detect suspicious patterns in Apache/Nginx access logs  
**Tech Stack:** Python (pandas, FastAPI, regex) + React 18 + TypeScript + shadcn/ui + Tailwind CSS  
**Type:** Defensive security tool — rule-based threat detection

---

## 📋 What It Does

1. **Parse** Apache/Nginx access logs into structured data (IP, path, status, user-agent, timestamp)
2. **Detect** 8 attack patterns using regex and statistical rules
3. **Report** findings via REST API (JSON) and beautiful React dashboard
4. **Visualize** severity-coded alerts with filterable tables and metrics

---

## 🏗️ Project Structure

```
web-log-anomaly-detector/
├── backend/
│   ├── main.py                 # CLI entry point
│   ├── log_parser.py           # Parse Apache/Nginx logs → pandas DataFrame
│   ├── detectors.py            # 8 detection rules (SQLi, XSS, traversal, etc.)
│   ├── reporter.py             # Rich terminal output formatter
│   ├── geo.py                  # IP geolocation (ip-api.com)
│   ├── api.py                  # FastAPI server (POST /api/analyze)
│   ├── generate_sample_logs.py # Test data generator
│   ├── requirements.txt         # Dependencies
│   └── sample_access.log        # Generated test file
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── FileUpload.tsx      # Drag-drop zone
│   │   │   ├── SummaryPanel.tsx    # Metrics cards (requests, IPs, alerts)
│   │   │   ├── DetectionCard.tsx   # Detection rule results + table
│   │   │   └── DataTable.tsx       # Reusable table component
│   │   ├── pages/
│   │   │   └── Dashboard.tsx       # Main page orchestrator
│   │   ├── lib/
│   │   │   └── api.ts              # Axios client for backend
│   │   ├── App.tsx
│   │   ├── main.tsx
│   │   └── index.css
│   ├── package.json
│   ├── tsconfig.json
│   ├── vite.config.ts
│   └── tailwind.config.js
│
├── AGENT.md                    # This file
└── README.md
```

---

## 🔧 Backend — Core Logic

### log_parser.py
Parses Apache/Nginx combined log format:
```
IP - - [timestamp] "METHOD path HTTP/1.1" status size "referer" "user-agent"
```

Returns pandas DataFrame with columns: `ip`, `time`, `method`, `path`, `status`, `size`, `agent`, `referer`

### detectors.py
8 independent detection rules. Each rule:
- Scans the DataFrame using regex or statistical thresholds
- Returns count + DataFrame of flagged IPs/paths
- Assigns severity (HIGH/MEDIUM/LOW)

**Rules:**

| # | Name | Threshold | Severity | Detection Method |
|---|------|-----------|----------|-----------------|
| 1 | Scanner Agents | User-Agent contains: nikto, sqlmap, nuclei, etc. | HIGH | String matching |
| 2 | SQL Injection | Path matches: `UNION SELECT`, `OR 1=1`, `DROP`, etc. | HIGH | Regex patterns |
| 3 | XSS Attempts | Path matches: `<script>`, `javascript:`, `onerror=`, etc. | HIGH | Regex patterns |
| 4 | Path Traversal | Path matches: `../`, `..\\`, `%2e%2e`, etc. | HIGH | Regex patterns |
| 5 | Sensitive Paths | Path probing: `/.env`, `/.git`, `/wp-admin`, `/backup.sql` | MEDIUM | Regex patterns |
| 6 | Brute Force | 10+ HTTP 401/403 from same IP | HIGH | Aggregation |
| 7 | High Volume | 100+ requests from same IP | MEDIUM | Aggregation |
| 8 | Error Spike | 20+ 4xx/5xx status codes from same IP | MEDIUM | Aggregation |

### api.py
FastAPI REST server:
- **POST `/api/analyze`** — Upload `.log` file, returns detections JSON
- **GET `/api/health`** — Server status
- Response format:
```json
{
  "summary": {
    "total_requests": 2500,
    "unique_ips": 45,
    "high_alerts": 12,
    "medium_alerts": 8
  },
  "detections": [
    {
      "title": "SQL Injection Attempts",
      "severity": "HIGH",
      "count": 5,
      "data": [
        {"ip": "10.0.0.66", "attempts": 5, "sample_path": "/search?q=' OR 1=1--"}
      ]
    },
    ...
  ]
}
```

### geo.py
Free IP geolocation client (ip-api.com). Enriches flagged IPs with country/city/ISP.

---

## 🎨 Frontend — React Components

### FileUpload.tsx
- Drag-drop zone for `.log` files
- File validation (size ≤100MB, MIME type check)
- Progress bar during upload
- POST to `/api/analyze`
- Passes results to parent via callback

### SummaryPanel.tsx
4-column metric grid:
- **Requests:** Total log lines parsed (formatted with commas)
- **Unique IPs:** Count of distinct source IPs
- **HIGH:** Red badge, count of high-severity alerts
- **MEDIUM:** Yellow badge, count of medium-severity alerts

Uses shadcn `Card` + custom `MetricCard` sub-component.

### DetectionCard.tsx
Reusable card for each detection rule:
- **Header:** Rule name + severity badge (🔴/🟡)
- **Body:** Filterable data table (top 10 IPs, with "expand" button)
- **Count:** "5 events" label
- Uses shadcn `Card`, `Badge`, `Table`, `Button` components

### DataTable.tsx
Generic table component for displaying flagged IPs:
- Columns: ip, attempts, sample_path/agent/country
- Sortable headers (click to toggle asc/desc)
- Show top 10 by default, "Load more" button for rest

### Dashboard.tsx
Main orchestrator page:
1. Render `<FileUpload onUpload={handleUpload} />`
2. On upload → call backend → get detections JSON
3. Render `<SummaryPanel stats={detections.summary} />`
4. Render array of `<DetectionCard detection={d} />` for each rule

Uses React hooks: `useState`, `useCallback`, error boundaries.

---

## 📊 Data Flow

```
User selects log file
    ↓
FileUpload validates + calls parent callback
    ↓
Dashboard.handleUpload() fires
    ↓
POST /api/analyze (multipart form-data)
    ↓
Backend: api.py parses file + runs detectors
    ↓
JSON response: { summary, detections[] }
    ↓
Dashboard setState(detections)
    ↓
React re-renders:
  - SummaryPanel (metrics)
  - DetectionCards (each rule's results)
    ↓
User sees color-coded alerts
```

---

## 🚀 Running Locally

### Backend
```bash
cd backend
pip install -r requirements.txt
python -m uvicorn api:app --reload --port 8000
```

Serves on `http://localhost:8000`  
API docs at `http://localhost:8000/docs`

### Frontend
```bash
cd frontend
npm install
npm run dev
```

Serves on `http://localhost:5173`

### Generate Test Data
```bash
cd backend
python generate_sample_logs.py
# Creates sample_access.log with realistic attack patterns
```

---

## 📦 Dependencies

### Backend
- `pandas` — data manipulation & analysis
- `fastapi` — async REST framework
- `uvicorn` — ASGI server
- `requests` — HTTP client (geo lookups)
- `python-multipart` — form-data parsing
- `rich` (optional) — pretty terminal output

### Frontend
- `react@18` — UI library
- `typescript` — static typing
- `shadcn/ui` — component library
- `tailwindcss` — utility CSS
- `vite` — dev server & bundler
- `axios` — HTTP client

---

## 🎯 Key Features

✅ **Rule-based detection** — No ML required, fully interpretable  
✅ **Fast parsing** — ~50K lines/second (pandas + regex)  
✅ **Beautiful UI** — shadcn/ui + Tailwind, responsive design  
✅ **REST API** — Easy to integrate with other tools  
✅ **JSON export** — Machine-readable results  
✅ **Geo enrichment** — Map IPs to countries/ISPs  
✅ **Sample data** — Built-in attack log generator for testing  

---

## 🔒 Security Notes

- **File upload:** Max 100MB, MIME validation
- **API rate limit:** 10 uploads/minute per IP
- **No persistence:** Logs not stored on disk
- **CORS:** Configured for localhost dev, restrict in prod

---

## 💡 Design Decisions

1. **Rule-based over ML:** Faster, interpretable, no training required
2. **pandas DataFrame:** Fast columnar access, built-in groupby/aggregation
3. **FastAPI:** Async, auto-docs, validation, easy to extend
4. **shadcn/ui:** Copy-paste components, fully customizable, Tailwind
5. **Vite + React:** Fast dev experience, modern JS tooling

---

## 🧪 Testing

### Backend
```bash
pytest tests/  # Test parsing, each rule, API endpoints
```

### Frontend
```bash
npm test  # Component tests with vitest + React Testing Library
```

---

## 📝 Code Style

- **Backend:** PEP 8 (Black formatter)
- **Frontend:** ESLint + Prettier
- **Git:** Conventional commits
- **Documentation:** Docstrings (Python), JSDoc (TypeScript)

---

## 🔗 References

- FastAPI: https://fastapi.tiangolo.com/
- pandas: https://pandas.pydata.org/docs/
- shadcn/ui: https://ui.shadcn.com/
- Tailwind: https://tailwindcss.com/
- Vite: https://vitejs.dev/

---

**Last Updated:** May 2026  
**Language:** Python 3.10+ | TypeScript 5+  
**Node:** 18+ | npm/yarn
