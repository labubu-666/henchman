import pytest
import yaml

from src.schema import load_deployment


def test_load_empty_deployment():
    deployment = load_deployment("""
    """)

    assert deployment is None


def test_load_single_service_with_image():
    deployment = load_deployment("""
services:
  service-1:
    image: image-1:latest
    """)

    assert deployment is not None
    assert isinstance(deployment.services, dict)
    assert "service-1" in deployment.services
    assert deployment.services["service-1"].image == "image-1:latest"
    container_name = "test_service-1_1"
    assert deployment.services["service-1"].build_run_command(
        container_name=container_name
    ) == ["docker", "run", "--name", "test_service-1_1", "--rm", "image-1:latest"]
