import os
import tempfile
from typing import Any

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from detectors import detect_all
from log_parser import parse_log_file

MAX_UPLOAD_BYTES = 100 * 1024 * 1024

app = FastAPI(title="Web Log Anomaly Detector API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def _build_response(df, results: dict[str, dict[str, Any]]) -> dict[str, Any]:
    high_alerts = sum(
        1 for r in results.values() if r["severity"] == "HIGH" and r["count"] > 0
    )
    medium_alerts = sum(
        1 for r in results.values() if r["severity"] == "MEDIUM" and r["count"] > 0
    )

    detections = []
    for key, result in results.items():
        data_df = result["data"]
        columns = list(data_df.columns) if data_df is not None and not data_df.empty else []
        rows = data_df.to_dict(orient="records") if columns else []
        detections.append(
            {
                "key": key,
                "title": result["title"],
                "severity": result["severity"],
                "count": int(result["count"]),
                "columns": columns,
                "data": rows,
            }
        )

    return {
        "summary": {
            "total_requests": int(len(df)),
            "unique_ips": int(df["ip"].nunique()) if not df.empty else 0,
            "high_alerts": high_alerts,
            "medium_alerts": medium_alerts,
        },
        "detections": detections,
    }


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/api/analyze")
async def analyze(file: UploadFile = File(...)) -> dict[str, Any]:
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file uploaded.")

    content = await file.read()
    if len(content) > MAX_UPLOAD_BYTES:
        raise HTTPException(status_code=413, detail="File exceeds 100 MB limit.")
    if not content.strip():
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")

    tmp_path = ""
    try:
        with tempfile.NamedTemporaryFile(mode="wb", suffix=".log", delete=False) as tmp:
            tmp.write(content)
            tmp_path = tmp.name

        df = parse_log_file(tmp_path)
    finally:
        if tmp_path and os.path.exists(tmp_path):
            os.unlink(tmp_path)

    if df.empty:
        raise HTTPException(
            status_code=400,
            detail="No valid log entries parsed. Check the log format.",
        )

    results = detect_all(df)
    return _build_response(df, results)
