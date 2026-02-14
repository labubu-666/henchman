import pytest


@pytest.fixture
def empty_tmpfile(tmp_path):
    p = tmp_path / "example.yml"
    # create an empty YAML file (as per current example)
    p.write_text("", encoding="utf-8")
    return p
