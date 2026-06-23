import hashlib
import mimetypes
from pathlib import Path

from ctf_toolkit.modules.hashing.hash_tools import normalize_algorithm


def _get_file_path(file_path: str) -> Path:
    """
    Converts string path to Path object and checks if the file exists.
    """
    if not isinstance(file_path, str):
        raise TypeError("File path must be a string.")

    cleaned_path = file_path.strip().strip('"').strip("'")
    path = Path(cleaned_path)

    if not path.exists():
        raise FileNotFoundError(f"File does not exist: {file_path}")

    if not path.is_file():
        raise ValueError(f"Path is not a file: {file_path}")

    return path


def get_file_info(file_path: str) -> dict[str, object]:
    """
    Returns basic information about a file.
    """
    path = _get_file_path(file_path)
    mime_type, _ = mimetypes.guess_type(path.name)

    return {
        "name": path.name,
        "path": str(path),
        "extension": path.suffix if path.suffix else "no extension",
        "size_bytes": path.stat().st_size,
        "mime_type": mime_type if mime_type else "unknown",
    }


def calculate_file_hash(file_path: str, algorithm: str = "sha256") -> str:
    """
    Calculates hash of a file.

    Example algorithms:
        md5
        sha1
        sha256
        sha512
    """
    path = _get_file_path(file_path)
    normalized_algorithm = normalize_algorithm(algorithm)

    hash_object = hashlib.new(normalized_algorithm)

    with path.open("rb") as file:
        while True:
            chunk = file.read(8192)

            if not chunk:
                break

            hash_object.update(chunk)

    return hash_object.hexdigest()


def extract_printable_strings(file_path: str, min_length: int = 4) -> list[str]:
    """
    Extracts readable ASCII strings from a file.

    Useful for simple CTF/forensics tasks.
    """
    if not isinstance(min_length, int):
        raise TypeError("Minimum length must be an integer.")

    if min_length <= 0:
        raise ValueError("Minimum length must be greater than zero.")

    path = _get_file_path(file_path)

    found_strings = []
    current_chars = []

    with path.open("rb") as file:
        data = file.read()

    for byte in data:
        if 32 <= byte <= 126:
            current_chars.append(chr(byte))
        else:
            if len(current_chars) >= min_length:
                found_strings.append("".join(current_chars))

            current_chars = []

    if len(current_chars) >= min_length:
        found_strings.append("".join(current_chars))

    return found_strings