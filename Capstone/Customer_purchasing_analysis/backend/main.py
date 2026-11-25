import os
import shutil
import uuid
import time
import httpx
from pathlib import Path
from typing import Optional, Dict, Any
from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Request, Response, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from pydantic import BaseModel

# Configuration from environment variables
RSCRIPT_PATH = os.environ.get("RSCRIPT_PATH", r"C:\Program Files\R\R-4.6.2\bin\Rscript.exe")
SESSION_DIR = Path(os.environ.get("SESSION_DIR", str(Path(__file__).resolve().parent.parent / "temp_sessions")))
R_SERVICE_URL = os.environ.get("R_SERVICE_URL", "http://127.0.0.1:8001")
MAX_FILE_SIZE_BYTES = 100 * 1024 * 1024  # 100 MB
SESSION_EXPIRY_SECONDS = 8 * 3600  # 8 hours

SESSION_DIR.mkdir(parents=True, exist_ok=True)

app = FastAPI(
    title="Customer Clickstream Analytics Backend",
    description="Python FastAPI Orchestrator for R Analytics Engine",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173", "http://localhost:3000", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def cleanup_expired_sessions():
    """Remove session directories older than 8 hours."""
    now = time.time()
    try:
        for item in SESSION_DIR.iterdir():
            if item.is_dir():
                mtime = item.stat().st_mtime
                if now - mtime > SESSION_EXPIRY_SECONDS:
                    shutil.rmtree(item, ignore_errors=True)
    except Exception as e:
        print(f"[Cleanup Error] {e}")

def get_or_create_session(request: Request, response: Response) -> str:
    """Retrieve session id from cookie or header, or create a new secure session."""
    cleanup_expired_sessions()
    session_id = request.cookies.get("capstone_session_id") or request.headers.get("X-Session-Id")
    if not session_id or not session_id.isalnum() or len(session_id) > 64:
        session_id = uuid.uuid4().hex
        response.set_cookie(
            key="capstone_session_id",
            value=session_id,
            httponly=True,
            samesite="lax",
            max_age=SESSION_EXPIRY_SECONDS
        )
    
    session_path = SESSION_DIR / session_id
    session_path.mkdir(parents=True, exist_ok=True)
    return session_id

def get_session_dir(session_id: str) -> Path:
    safe_id = "".join(c for c in session_id if c.isalnum() or c in "-_")
    path = SESSION_DIR / safe_id
    if not path.resolve().is_relative_to(SESSION_DIR.resolve()):
        raise HTTPException(status_code=400, detail="Invalid session path traversal")
    path.mkdir(parents=True, exist_ok=True)
    return path

# Health check
@app.get("/api/health")
async def health(session_id: str = Depends(get_or_create_session)):
    r_status = "unreachable"
    r_info = {}
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            resp = await client.get(f"{R_SERVICE_URL}/health")
            if resp.status_code == 200:
                r_status = "healthy"
                r_info = resp.json()
    except Exception as e:
        r_status = f"unreachable: {str(e)}"

    session_path = get_session_dir(session_id)
    raw_exists = (session_path / "raw_clickstream.csv").exists()
    cleaned_exists = (session_path / "cleaned_clickstream.csv").exists()

    return {
        "status": "ok",
        "session_id": session_id,
        "r_service": {
            "status": r_status,
            "url": R_SERVICE_URL,
            "info": r_info
        },
        "dataset_status": {
            "raw_uploaded": raw_exists,
            "cleaned_available": cleaned_exists,
            "active_file": "cleaned_clickstream.csv" if cleaned_exists else ("raw_clickstream.csv" if raw_exists else None)
        }
    }

# Load sample dataset automatically from repo into current session
@app.post("/api/dataset/load-default")
async def load_default_dataset(session_id: str = Depends(get_or_create_session)):
    default_dataset = Path(__file__).resolve().parent.parent / "dataset" / "customer_clickstream_purchase_dataset.csv"
    if not default_dataset.exists():
        raise HTTPException(status_code=404, detail="Default dataset file not found on server")
    
    session_path = get_session_dir(session_id)
    target = session_path / "raw_clickstream.csv"
    shutil.copyfile(default_dataset, target)

    # Inform R about the uploaded file
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            r_resp = await client.post(
                f"{R_SERVICE_URL}/dataset/inspect",
                json={"session_id": session_id}
            )
            inspect_data = r_resp.json() if r_resp.status_code == 200 else {}
    except Exception as e:
        inspect_data = {"error": f"R inspection failed: {str(e)}"}

    return {
        "status": "success",
        "message": "Default dataset loaded into session successfully",
        "file_size": target.stat().st_size,
        "inspection": inspect_data
    }

# CSV Upload handler with streaming validation and safe writes
@app.post("/api/dataset/upload")
async def upload_dataset(
    file: UploadFile = File(...),
    session_id: str = Depends(get_or_create_session)
):
    if not file.filename.lower().endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are supported")
    
    session_path = get_session_dir(session_id)
    target_path = session_path / "raw_clickstream.csv"
    cleaned_path = session_path / "cleaned_clickstream.csv"

    # Remove previous cleaned file if a new file is uploaded
    if cleaned_path.exists():
        cleaned_path.unlink()

    total_bytes = 0
    first_chunk = True
    header_line = ""

    with open(target_path, "wb") as f_out:
        while True:
            chunk = await file.read(64 * 1024)
            if not chunk:
                break
            total_bytes += len(chunk)
            if total_bytes > MAX_FILE_SIZE_BYTES:
                target_path.unlink(missing_ok=True)
                raise HTTPException(status_code=413, detail=f"File exceeds maximum allowed size of {MAX_FILE_SIZE_BYTES // (1024*1024)}MB")
            if first_chunk:
                decoded = chunk.decode("utf-8", errors="ignore")
                lines = decoded.splitlines()
                if lines:
                    header_line = lines[0]
                first_chunk = False
            f_out.write(chunk)

    if total_bytes == 0:
        target_path.unlink(missing_ok=True)
        raise HTTPException(status_code=400, detail="Uploaded file is empty")

    # Ask R to inspect the new raw dataset
    inspect_data = {}
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            r_resp = await client.post(
                f"{R_SERVICE_URL}/dataset/inspect",
                json={"session_id": session_id}
            )
            if r_resp.status_code == 200:
                inspect_data = r_resp.json()
    except Exception as e:
        inspect_data = {"error": f"R inspection failed: {str(e)}"}

    return {
        "status": "success",
        "filename": file.filename,
        "bytes_received": total_bytes,
        "inspection": inspect_data
    }

# Clear dataset
@app.delete("/api/dataset/clear")
async def clear_dataset(session_id: str = Depends(get_or_create_session)):
    session_path = get_session_dir(session_id)
    for f in session_path.glob("*"):
        try:
            if f.is_file():
                f.unlink()
            elif f.is_dir():
                shutil.rmtree(f)
        except Exception:
            pass
    return {"status": "success", "message": "Session dataset cleared"}

# Save / Update Field Mapping
class FieldMappingPayload(BaseModel):
    mapping: Dict[str, str]

@app.post("/api/dataset/field-mapping")
async def save_field_mapping(payload: FieldMappingPayload, session_id: str = Depends(get_or_create_session)):
    async with httpx.AsyncClient(timeout=15.0) as client:
        resp = await client.post(
            f"{R_SERVICE_URL}/dataset/field-mapping",
            json={"session_id": session_id, "mapping": payload.mapping}
        )
        return resp.json()

# General Proxy to R Service for all analytics, ML, and queries
@app.api_route("/api/r/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def proxy_to_r(request: Request, path: str, session_id: str = Depends(get_or_create_session)):
    url = f"{R_SERVICE_URL}/{path}"
    body = None
    params = dict(request.query_params)

    if request.method in ["POST", "PUT"]:
        try:
            body = await request.json()
            if isinstance(body, dict):
                body["session_id"] = session_id
        except Exception:
            body = {"session_id": session_id}
        # Do not send in query string if in body to prevent vector coercion in R
        params.pop("session_id", None)
    else:
        params["session_id"] = session_id

    headers = {"X-Session-Id": session_id}

    try:
        async with httpx.AsyncClient(timeout=300.0) as client:
            resp = await client.request(
                method=request.method,
                url=url,
                params=params,
                json=body,
                headers=headers
            )
            try:
                return JSONResponse(status_code=resp.status_code, content=resp.json())
            except Exception:
                return Response(content=resp.content, status_code=resp.status_code, media_type=resp.headers.get("content-type", "application/json"))
    except httpx.RequestError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Error communicating with R analytics service on {R_SERVICE_URL}: {str(exc)}"
        )

# CSV Export Endpoint
@app.get("/api/export/csv")
async def export_csv(
    file_type: str,
    session_id: str = Depends(get_or_create_session)
):
    session_path = get_session_dir(session_id)
    filename_map = {
        "cleaned": "cleaned_clickstream.csv",
        "predictions": "conversion_predictions.csv",
        "revenue_predictions": "revenue_predictions.csv",
        "studio_export": "dynamic_chart_export.csv",
        "rfm_segments": "rfm_segments.csv"
    }
    filename = filename_map.get(file_type, f"{file_type}.csv")
    file_path = session_path / filename

    if not file_path.exists():
        raise HTTPException(status_code=404, detail=f"Export file '{filename}' not found for current session")
    
    return FileResponse(
        path=str(file_path),
        filename=filename,
        media_type="text/csv"
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
