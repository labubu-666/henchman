from typing import Dict, Optional

import yaml
from pydantic import BaseModel


def build_container_name(working_dir: str, service: str) -> str:
    return f"{working_dir}_{service}_1"


class Service(BaseModel):
    detached: bool
    image: str

    def build_run_command(self, container_name: str) -> list:
        """Build the docker run command for this service."""

        command = ["docker", "run", "--name", container_name, "--rm"]
        if bool(self.detached):
            # docker uses --detach (or -d) to run containers in the background
            command.append("--detach")
        command.append(self.image)
        return command

    def build_stop_command(self, container_name: str) -> list:
        # docker stop takes container names/ids as positional arguments
        return ["docker", "container", "stop", container_name]

    def build_remove_command(self, container_name: str) -> list:
        # docker stop takes container names/ids as positional arguments
        return ["docker", "container", "rm", container_name]


class Deployment(BaseModel):
    services: Optional[Dict[str, Service]] = None


def load_deployment(deployment_contents: str, detached: bool) -> Optional[Deployment]:
    if data := yaml.safe_load(deployment_contents):
        for name, service in data.get("services", {}).items():
            service.update({"detached": detached})

        return Deployment.model_validate(data)
    else:
        return None
