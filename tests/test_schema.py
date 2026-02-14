import pytest
import yaml

from src.schema import load_deployment


def test_load_empty_deployment():
    deployment = load_deployment("""
    """, detached=False)

    assert deployment is None


def test_build_run_command_for_single_attached_service_with_image():
    deployment = load_deployment("""
services:
  service-1:
    image: image-1:latest
    """, detached=False)

    assert deployment is not None
    assert isinstance(deployment.services, dict)
    assert "service-1" in deployment.services
    assert deployment.services["service-1"].image == "image-1:latest"
    container_name = "test_service-1_1"
    assert deployment.services["service-1"].build_run_command(
        container_name=container_name
    ) == ["docker", "run", "--name", "test_service-1_1", "--rm", "image-1:latest"]


def test_build_run_command_for_single_detached_service_with_image():
    deployment = load_deployment("""
services:
  service-1:
    image: image-1:latest
    """, detached=True)

    assert deployment is not None
    assert isinstance(deployment.services, dict)
    assert "service-1" in deployment.services
    assert deployment.services["service-1"].image == "image-1:latest"
    container_name = "test_service-1_1"
    assert deployment.services["service-1"].build_run_command(
        container_name=container_name
    ) == ["docker", "run", "--name", "test_service-1_1", "--rm", "--detach", "image-1:latest"]

def test_build_stop_command_for_single_detached_service_with_image():
    deployment = load_deployment("""
services:
  service-1:
    image: image-1:latest
    """, detached=True)

    assert deployment is not None
    assert isinstance(deployment.services, dict)
    assert "service-1" in deployment.services
    assert deployment.services["service-1"].image == "image-1:latest"
    container_name = "test_service-1_1"
    assert deployment.services["service-1"].build_stop_command(
        container_name=container_name
    ) == ["docker", "container", "stop", "test_service-1_1"]
