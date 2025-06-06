import docker

client = docker.from_env()

def run_docker_container(image, cmd=None, env=None, ports=None):
    container = client.containers.run(
        image=image,
        command=cmd,
        environment=env or {},
        ports=ports or {},
        detach=True
    )
    return container

def stop_and_remove_container(container_id):
    container = client.containers.get(container_id)
    container.stop()
    container.remove()
    return True

def get_logs_for_container(container_id):
    container = client.containers.get(container_id)
    return container.logs().decode()