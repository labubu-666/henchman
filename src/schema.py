from typing import Dict, Optional

import yaml
from pydantic import BaseModel


def build_container_name(working_dir: str, service: str) -> str:
    return f"{working_dir}_{service}_1"


class Service(BaseModel):
    image: str

    def build_run_command(self, container_name: str) -> list:
        return ["docker", "run", "--name", container_name, "--rm", self.image]

    def build_stop_command(self, container_name: str) -> list:
        return ["docker", "stop", "--name", container_name, self.image]


class Deployment(BaseModel):
    services: Optional[Dict[str, Service]] = None


def load_deployment(deployment_contents: str) -> Optional[Deployment]:
    if data := yaml.safe_load(deployment_contents):
        return Deployment.model_validate(data)
    else:
        return None
