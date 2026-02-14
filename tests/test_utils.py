import io
import sys

import pytest

from src.utils import read_file


def test_read_file_reads_content(empty_tmpfile):
    content = read_file(empty_tmpfile)
    assert content == ""


def test_read_file_reads_stdin(monkeypatch):
    # Simulate passing '-' to read from stdin
    monkeypatch.setattr(sys, "stdin", io.StringIO("a: 1\n"))
    content = read_file("-")
    assert content == "a: 1\n"
