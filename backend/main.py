from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from jobs import submit_whisper_job
from llama_runner import query_llama
from models import SubmitJobRequest, JobResponse
from job_executor import submit_job
from job_registry import get_job, get_logs_for_job, stop_and_remove_job
from fastapi.responses import PlainTextResponse
from uuid import uuid4
import httpx
import shutil
import psutil
import os
from dotenv import load_dotenv
load_dotenv()

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace "*" with specific domains if you want
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    prompt: str

@app.post("/chat")
async def chat(req: ChatRequest):
    response = await query_llama(req.prompt)
    return {"response": response}

@app.get("/health/ollama")
async def health_check():
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            r = await client.get(OLLAMA_HOST)
            return {"status": "OK", "ollama": r.status_code}
    except Exception as e:
        return {"status": "unavailable", "error": str(e)}

@app.get("/health")
async def full_health_check():
    status = {
        "server": "ok",
        "cpu_percent": psutil.cpu_percent(),
        "disk_usage_percent": shutil.disk_usage("/").used / shutil.disk_usage("/").total * 100,
    }

    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            r = await client.get(OLLAMA_HOST)
            status["ollama"] = "ok" if r.status_code == 200 else f"error {r.status_code}"
    except Exception as e:
        status["ollama"] = f"unavailable: {str(e)}"

    return status

# @app.post("/submit-whisper")
# async def submit_job(audio_file: UploadFile = File(...)):
#     job_id = str(uuid4())
#     contents = await audio_file.read()
#     with open(f"/tmp/{job_id}.mp3", "wb") as f:
#         f.write(contents)
#     submit_whisper_job(job_id, f"/tmp/{job_id}.mp3")
#     return {"job_id": job_id, "status": "submitted"}

# @app.get("/status/{job_id}")
# async def check_status(job_id: str):
#     try:
#         with open(f"/tmp/{job_id}.txt", "r") as f:
#             return {"status": "completed", "output": f.read()}
#     except FileNotFoundError:
#         return {"status": "pending or failed"}

@app.post("/jobs", response_model=JobResponse)
def submit_job_api(req: SubmitJobRequest):
    if req.type not in {"docker", "github"}:
        raise HTTPException(status_code=400, detail="Only docker or github jobs supported")
    try:
        job_id, container_id = submit_job(req)
        return JobResponse(job_id=job_id, container_id=container_id, status="running")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/jobs/{job_id}")
def get_job_status(job_id: str):
    job = get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job

@app.get("/jobs/{job_id}/logs", response_class=PlainTextResponse)
def get_logs(job_id: str):
    logs = get_logs_for_job(job_id)
    if logs is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return logs

@app.post("/jobs/{job_id}/stop")
def stop_job(job_id: str):
    success = stop_and_remove_job(job_id)
    if not success:
        raise HTTPException(status_code=404, detail="Job not found or already stopped")
    return {"status": "stopped"}