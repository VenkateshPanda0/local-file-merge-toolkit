"""
Path utilities — absolute project-root paths and folder helpers.
"""

import os
import re
from pathlib import Path


# ---------------------------------------------------------
# Base Paths
# ---------------------------------------------------------

BASE_DIR: Path = Path(__file__).resolve().parent.parent
OUTPUT_DIR: Path = BASE_DIR / "output"
LOG_DIR: Path = BASE_DIR / "logs"


# ---------------------------------------------------------
# Constants
# ---------------------------------------------------------

_ILLEGAL_CHARS = re.compile(r'[<>:"/\\|?*\x00-\x1f]')

_WINDOWS_RESERVED = {
    "con", "prn", "aux", "nul",
    "com1", "com2", "com3", "com4", "com5", "com6", "com7", "com8", "com9",
    "lpt1", "lpt2", "lpt3", "lpt4", "lpt5", "lpt6", "lpt7", "lpt8", "lpt9"
}

_IGNORED_FILES = {
    ".ds_store",
    "thumbs.db"
}


# ---------------------------------------------------------
# Folder Management
# ---------------------------------------------------------

def ensure_folders() -> None:
    """Create required folders."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    LOG_DIR.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------
# File Discovery
# ---------------------------------------------------------

def get_files_in_folder(
    folder_path: str,
    extensions: list[str]
) -> list[str]:
    """
    Return sorted matching files in folder (non-recursive).
    Case-insensitive extension matching.
    """

    folder = Path(folder_path)

    if not folder.exists() or not folder.is_dir():
        return []

    allowed = {ext.lower() for ext in extensions}
    results = []

    for item in folder.iterdir():
        if not item.is_file():
            continue

        name_lower = item.name.lower()

        if name_lower in _IGNORED_FILES:
            continue

        if name_lower.startswith("~$"):
            continue

        if item.suffix.lower() in allowed:
            results.append(str(item.resolve()))

    return sorted(results, key=lambda x: x.lower())


# ---------------------------------------------------------
# Filename Sanitization
# ---------------------------------------------------------

def sanitize_filename(name: str) -> str:
    """
    Sanitize user-supplied filename safely.
    Always returns usable filename stem.
    """

    # Remove traversal/path parts
    name = os.path.basename(name.strip())

    # Replace illegal chars
    name = _ILLEGAL_CHARS.sub("_", name)

    # Collapse underscores
    name = re.sub(r"_+", "_", name)

    # Remove leading/trailing junk
    name = name.strip(" ._")

    if not name:
        return "merged_file"

    stem, ext = os.path.splitext(name)

    if stem.lower() in _WINDOWS_RESERVED:
        stem = f"{stem}_file"

    cleaned = stem.strip() or "merged_file"

    return cleaned + ext