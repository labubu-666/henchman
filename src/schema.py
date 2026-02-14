from typing import Dict

import yaml
from pydantic import BaseModel


class Deployment:
    services: Dict[str, Service]


class Service(BaseModel):
    image: str


def load_deployment(deployment_contents: str):
    return yaml.safe_load(deployment_contents)
