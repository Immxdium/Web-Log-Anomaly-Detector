# Web Log Anomaly Detector

Rule-based security tool that parses Apache/Nginx access logs and surfaces suspicious activity — SQL injection, XSS, path traversal, scanner agents, brute force, and more — through a FastAPI backend and React dashboard.

## Features

- **8 detection rules** — regex and statistical thresholds for common web attack patterns
- **REST API** — upload a `.log` file, get structured JSON results
- **React dashboard** — drag-and-drop upload, severity-coded alerts, exportable reports
- **CLI mode** — analyze logs from the terminal with Rich-formatted output
- **Sample data** — included `backend/sample_access.log` with realistic attack traffic

## Detection Rules

| Rule | Severity | Method |
|------|----------|--------|
| Scanner user-agents | HIGH | String matching (nikto, sqlmap, nuclei, etc.) |
| SQL injection | HIGH | Regex patterns |
| XSS attempts | HIGH | Regex patterns |
| Path traversal | HIGH | Regex patterns |
| Sensitive path probing | MEDIUM | Regex patterns |
| Brute force (10+ 401/403) | HIGH | IP aggregation |
| High volume (100+ requests) | MEDIUM | IP aggregation |
| Error spike (20+ 4xx/5xx) | MEDIUM | IP aggregation |

## Tech Stack

**Backend:** Python 3.10+, pandas, FastAPI, uvicorn  
**Frontend:** React 19, TypeScript, Vite, Tailwind CSS v4, shadcn/ui

## Project Structure

```
Web-Log-Anomaly-Detector/
├── backend/
│   ├── api.py              # FastAPI server (POST /api/analyze)
│   ├── detectors.py        # 8 detection rules
│   ├── log_parser.py       # Apache/Nginx log parser
│   ├── main.py             # CLI entry point
│   ├── reporter.py         # Terminal output formatter
│   ├── geo.py              # IP geolocation (ip-api.com)
│   ├── generate_sample_logs.py
│   └── sample_access.log
└── frontend/
    └── src/
        ├── components/     # UploadZone, DetectionCard, SummaryPanel, etc.
        ├── lib/api.ts        # Axios client
        └── App.tsx           # Main dashboard
```

## Getting Started

### Prerequisites

- Python 3.10+
- Node.js 18+

### Backend

```bash
cd backend
python -m venv ../env
source ../env/bin/activate   # Windows: ..\env\Scripts\activate
pip install -r requirements.txt
python -m uvicorn api:app --reload --port 8000
```

API docs: http://localhost:8000/docs

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Dashboard: http://localhost:5173

The Vite dev server proxies `/api` requests to the backend on port 8000.

### CLI (no UI)

```bash
cd backend
source ../env/bin/activate
python main.py sample_access.log
python main.py sample_access.log --json
python main.py sample_access.log --geo
```

## API

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/health` | Server status |
| `POST` | `/api/analyze` | Upload `.log` file (multipart form, max 100 MB) |

**Example response:**

```json
{
  "summary": {
    "total_requests": 2055,
    "unique_ips": 24,
    "high_alerts": 5,
    "medium_alerts": 3
  },
  "detections": [
    {
      "key": "sqli",
      "title": "SQL injection attempts",
      "severity": "HIGH",
      "count": 4,
      "columns": ["ip", "attempts", "sample_path"],
      "data": [{ "ip": "10.0.0.66", "attempts": 4, "sample_path": "/login?user=admin'--" }]
    }
  ]
}
```

## Generate Sample Logs

```bash
cd backend
python generate_sample_logs.py
```

## License

MIT
