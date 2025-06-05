from fastapi import FastAPI, UploadFile, File
from jobs import submit_whisper_job
from uuid import uuid4

app = FastAPI()

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
