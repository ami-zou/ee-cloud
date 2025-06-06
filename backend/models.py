from pydantic import BaseModel, HttpUrl, Field
from typing import Optional, Dict, Literal

class SubmitJobRequest(BaseModel):
    type: Literal["docker", "github"]
    image: Optional[str] = None
    repo: Optional[HttpUrl] = None
    startup_cmd: Optional[str] = None
    expose_port: Optional[int] = 7860
    env: Optional[Dict[str, str]] = Field(default_factory=dict)

class JobResponse(BaseModel):
    job_id: str
    container_id: str
    status: str