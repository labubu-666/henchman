from pathlib import Path
from typing import Union
import sys


def read_file(path: Union[str, Path]) -> str:
    # Support reading from stdin when the caller passes '-' (common CLI convention)
    if isinstance(path, str) and path == "-":
        return sys.stdin.read()

    p = Path(path)
    # Ensure the path points to an actual file (not a directory)
    if not p.is_file():
        raise FileNotFoundError(f"File not found: {p}")

    return p.read_text(encoding="utf-8")
