"""
Logging utilities.
Writes timestamped actions/failures to logs/history.log
"""

import datetime
from pathlib import Path

from utils.paths import LOG_DIR


LOG_FILE: Path = LOG_DIR / "history.log"


def _clean_message(message: str) -> str:
    """Convert multiline messages into one clean log line."""
    return " ".join(str(message).split()).strip()


def _write(level: str, message: str) -> None:
    """
    Internal logger writer.
    Never crashes main program.
    """

    try:
        LOG_DIR.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        clean = _clean_message(message)

        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(f"{timestamp} [{level}] {clean}\n")

    except Exception:
        # Logging must never break main workflow
        pass


def log_action(message: str) -> None:
    """Log successful actions."""
    _write("OK", message)


def log_failure(message: str) -> None:
    """Log failures."""
    _write("FAILED", message)


def log_warning(message: str) -> None:
    """Log warnings."""
    _write("WARN", message)