from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from jobs import submit_whisper_job
from llama_runner import query_llama
from uuid import uuid4
import httpx
import shutil
import psutil
import os
from dotenv import load_dotenv
load_dotenv()

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")

app = FastAPI()

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

@app.post("/submit-whisper")
async def submit_job(audio_file: UploadFile = File(...)):
    job_id = str(uuid4())
    contents = await audio_file.read()
    with open(f"/tmp/{job_id}.mp3", "wb") as f:
        f.write(contents)
    submit_whisper_job(job_id, f"/tmp/{job_id}.mp3")
    return {"job_id": job_id, "status": "submitted"}

@app.get("/status/{job_id}")
async def check_status(job_id: str):
    try:
        with open(f"/tmp/{job_id}.txt", "r") as f:
            return {"status": "completed", "output": f.read()}
    except FileNotFoundError:
        return {"status": "pending or failed"}
