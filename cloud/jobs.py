import subprocess
import threading

def submit_whisper_job(job_id: str, filepath: str):
    def run():
        try:
            result = subprocess.run(
                ["whisper", filepath, "--model", "base", "--output_format", "txt", "--output_dir", "/tmp"],
                capture_output=True,
                text=True,
            )
            if result.returncode != 0:
                with open(f"/tmp/{job_id}.txt", "w") as f:
                    f.write("ERROR: " + result.stderr)
        except Exception as e:
            with open(f"/tmp/{job_id}.txt", "w") as f:
                f.write(f"Exception occurred: {str(e)}")

    thread = threading.Thread(target=run)
    thread.start()
