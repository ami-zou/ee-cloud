from utils.docker_helper import stop_and_remove_container, get_logs_for_container
job_store = {}

def register_job(job_id, container_id):
    job_store[job_id] = {
        "container_id": container_id,
        "status": "running"
    }

def get_job(job_id):
    return job_store.get(job_id)

def stop_and_remove_job(job_id):
    job = job_store.get(job_id)
    if not job:
        return None
    stop_and_remove_container(job["container_id"])
    job["status"] = "stopped"
    return True

def get_logs_for_job(job_id):
    job = job_store.get(job_id)
    if not job:
        return None
    return get_logs_for_container(job["container_id"])