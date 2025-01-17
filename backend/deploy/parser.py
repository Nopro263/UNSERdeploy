from .models import _Install, Configuration

import yaml
import docker
from pathlib import Path
import os
import subprocess

ROOT_PATH = Path(".").resolve()

client = docker.DockerClient(base_url='unix://var/run/docker.sock')

def create_deployment(name: str, configuration: Configuration):
    if not (ROOT_PATH / name).is_relative_to(ROOT_PATH):
        raise Exception("invalid name")

    if os.path.exists(ROOT_PATH / name):
        raise Exception("project exists")
    
    os.mkdir(ROOT_PATH / name)
    os.chdir(ROOT_PATH / name)

    def g(nums: list[int]) -> str:
        s = ""
        for n in nums:
            s += f"EXPOSE {n}\n"
        return s
    
    def c(install) -> str:
        s = ""
        if isinstance(install, list):
            for i in install:
                s += f"RUN {i}\n"
        elif isinstance(install, _Install):
            for f in install.files:
                if os.path.basename(f) == f:
                    s += f"COPY {f} .\n"
                else:
                    s += f"RUN mkdir {os.path.basename(f)}\n"
                    s += f"COPY {f} {os.path.basename(f)}\n"
            
            for i in install.script:
                s += f"RUN {i}\n"
        
        return s

    with open("Dockerfile", "w") as f:
        f.write(f"""FROM {configuration.runtime.type}:{configuration.runtime.version}

{g(configuration.runtime.expose)}

WORKDIR {configuration.runtime.root}

{c(configuration.install)}


ENTRYPOINT [ "bash" ]""")
        
    client.images.build(path=".", tag=f"base/{name}")

    client.containers.run()

def _create_deployment(name: str, git_url: str):
    if not (ROOT_PATH / name).is_relative_to(ROOT_PATH):
        raise Exception("invalid name")

    if os.path.exists(ROOT_PATH / name):
        raise Exception("project exists")
    
    os.mkdir(ROOT_PATH / name)
    os.chdir(ROOT_PATH / name)

    
    subprocess.call([
        "git",
        "clone",
        git_url,
        "."
    ])

def parse_text(data: str) -> Configuration:
    raw = yaml.safe_load(data)

    root = Configuration.model_validate(raw)
    return root