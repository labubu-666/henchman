
from pathlib import Path
from typing import Union, Any
import sys


def read_yml_file(path: Union[str, Path]) -> str:
	"""
	Read and return the contents of a YAML file using pathlib.

	This function only reads the file as text. It validates that the file
	exists and has a .yml or .yaml extension.

	Args:
		path: Path or string pointing to a .yml/.yaml file.

	Returns:
		The file contents as a string.

	Raises:
		FileNotFoundError: If the file does not exist.
		ValueError: If the file extension is not .yml or .yaml.
	"""
	# Support reading from stdin when the caller passes '-' (common CLI convention)
	if isinstance(path, str) and path == "-":
		return sys.stdin.read()

	p = Path(path)
	# Ensure the path points to an actual file (not a directory)
	if not p.is_file():
		raise FileNotFoundError(f"YAML file not found: {p}")
	return p.read_text(encoding="utf-8")


def read_yml_parsed(path: Union[str, Path]) -> Any:
	"""
	Read and parse a YAML file into Python objects using PyYAML.

	This requires the 'yaml' package (PyYAML). If it's not installed a
	RuntimeError will be raised explaining how to install it.

	Args:
		path: Path or string pointing to a .yml/.yaml file.

	Returns:
		The Python object resulting from yaml.safe_load on the file contents.
	"""
	try:
		import yaml  # type: ignore
	except Exception as exc:  # ImportError or similar
		raise RuntimeError(
			"PyYAML is required to parse YAML. Install with: pip install pyyaml"
		) from exc

	text = read_yml_file(path)
	return yaml.safe_load(text)
