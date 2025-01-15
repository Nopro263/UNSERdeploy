from fastapi import HTTPException

import docker
from pathlib import Path
import os
import subprocess

ROOT_PATH = Path(".").resolve()

client = docker.DockerClient(base_url='unix://var/run/docker.sock')

def create_deployment(name: str, git_url: str):
    if not (ROOT_PATH / name).is_relative_to(ROOT_PATH):
        raise HTTPException(status_code=400, detail="invalid name")

    if os.path.exists(ROOT_PATH / name):
        raise HTTPException(status_code=400, detail="path exists already")
    
    os.mkdir(ROOT_PATH / name)
    os.chdir(ROOT_PATH / name)

    
    subprocess.call([
        "git",
        "clone",
        git_url,
        "."
    ])

    client.images.build(path=".", tag=f"build/{name}")

    client.containers.run()