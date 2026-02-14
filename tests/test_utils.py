import io
import sys

import pytest

from src.utils import read_yml_file, read_yml_parsed


@pytest.fixture
def tmpfile(tmp_path):
    p = tmp_path / "example.yml"
    # create an empty YAML file (as per current example)
    p.write_text("", encoding="utf-8")
    return p


def test_read_yml_file_reads_content(tmpfile):
    content = read_yml_file(tmpfile)
    assert content == ""


def test_read_yml_parsed_returns_none_for_empty(tmpfile):
    # Parsing an empty YAML file should return None when using PyYAML
    try:
        parsed = read_yml_parsed(tmpfile)
    except RuntimeError:
        pytest.skip("PyYAML not installed")
    assert parsed is None


def test_read_yml_file_reads_stdin(monkeypatch):
    # Simulate passing '-' to read from stdin
    monkeypatch.setattr(sys, 'stdin', io.StringIO("a: 1\n"))
    content = read_yml_file("-")
    assert content == "a: 1\n"
