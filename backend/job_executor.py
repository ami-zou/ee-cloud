import uuid
import os
import subprocess
from utils.docker_helper import run_docker_container, stop_and_remove_container, get_logs_for_container
from job_registry import register_job, get_job, stop_and_remove_job, get_logs_for_job

def submit_job(data):
    job_id = str(uuid.uuid4())

    if data.type == "docker":
        container = run_docker_container(
            image=data.image,
            env=data.env,
            ports={f"{data.expose_port}/tcp": data.expose_port}
        )
    elif data.type == "github":
        repo_dir = f"/tmp/job-{job_id}"
        subprocess.run(["git", "clone", data.repo, repo_dir], check=True)
        dockerfile_path = os.path.join(repo_dir, "Dockerfile")

        image_tag = f"user/job-{job_id}"
        subprocess.run(["docker", "build", "-t", image_tag, repo_dir], check=True)

        container = run_docker_container(
            image=image_tag,
            cmd=data.startup_cmd,
            env=data.env,
            ports={f"{data.expose_port}/tcp": data.expose_port}
        )
    else:
        raise ValueError("Invalid job type")

    register_job(job_id, container.id)
    return job_id, container.id

def stop_job(self, job_id: str):
    container = get_container(job_id)
    if container:
        stop_and_remove_container(container)
        remove_job(job_id)

def get_logs(self, job_id: str) -> str:
    container = get_container(job_id)
    if container:
        return get_logs_for_container(container)
    return "Job not found"


