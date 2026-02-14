import pytest
import yaml

from src.utils import read_file
from src.schema import load_deployment


def test_load_empty_deployment(empty_tmpfile):
    parsed = read_file(empty_tmpfile)

    deployment = load_deployment(parsed)

    assert deployment is None
