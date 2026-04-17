"""
SHA-256 file hashing utilities.
"""

import hashlib
from pathlib import Path


def calculate_sha256(file_path: str) -> str:
    """
    Calculate SHA-256 hash of a file using streamed reads.

    Raises:
        FileNotFoundError
        PermissionError
        IsADirectoryError
        OSError
    """

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    if path.is_dir():
        raise IsADirectoryError(f"Expected file, got directory: {file_path}")

    sha256 = hashlib.sha256()

    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            sha256.update(chunk)

    return sha256.hexdigest()