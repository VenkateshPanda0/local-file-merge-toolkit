from pathlib import Path

from utils.logger import log_action, log_failure
from utils.ui import print_warning


def _read_text_file(file_path: str) -> list[str]:
    """
    Read text file using common encodings.
    Returns lines without newline endings.
    """

    encodings = ["utf-8", "utf-16", "latin-1"]

    for enc in encodings:
        try:
            with open(file_path, "r", encoding=enc) as f:
                return [line.rstrip("\r\n") for line in f.readlines()]
        except Exception:
            continue

    raise ValueError("Unsupported or unreadable encoding")


def merge_text(
    file_list: list[str],
    output_path: str,
    separator: str = "=" * 40,
    remove_duplicates: bool = False,
    sort_lines: bool = False,
) -> None:
    """
    Merge text-based files.

    Supports:
    - .txt
    - .log
    - .md

    Features:
    - separator between files
    - remove duplicate lines
    - sort lines globally
    """

    merged_blocks: list[list[str]] = []

    successful_files = 0
    skipped_files = 0

    # ---------------------------------------------------------
    # Read files
    # ---------------------------------------------------------
    for file_path in file_list:
        try:
            lines = _read_text_file(file_path)

            if lines:
                merged_blocks.append(lines)

            successful_files += 1

        except Exception as e:
            print_warning(f"Skipping {file_path}: {e}")
            log_failure(f"Text file skipped: {file_path} ({e})")
            skipped_files += 1

    if not merged_blocks:
        raise ValueError("No valid text content found to merge.")

    # ---------------------------------------------------------
    # Flatten with separators only if not sorting
    # ---------------------------------------------------------
    merged_lines: list[str] = []

    for idx, block in enumerate(merged_blocks):
        merged_lines.extend(block)

        if (
            separator
            and not sort_lines
            and idx < len(merged_blocks) - 1
        ):
            merged_lines.append(separator)

    # ---------------------------------------------------------
    # Remove duplicates
    # ---------------------------------------------------------
    if remove_duplicates:
        seen = set()
        unique_lines = []

        for line in merged_lines:
            if line == separator:
                unique_lines.append(line)
                continue

            key = line.strip().lower()

            if key not in seen:
                seen.add(key)
                unique_lines.append(line)

        merged_lines = unique_lines

    # ---------------------------------------------------------
    # Sort globally (separators absent here)
    # ---------------------------------------------------------
    if sort_lines:
        merged_lines = sorted(merged_lines, key=str.lower)

    # ---------------------------------------------------------
    # Save
    # ---------------------------------------------------------
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8", newline="\n") as f:
        for line in merged_lines:
            f.write(line + "\n")

    # ---------------------------------------------------------
    # Log
    # ---------------------------------------------------------
    log_action(
        "Text merge success | "
        f"files_used={successful_files} "
        f"files_skipped={skipped_files} "
        f"lines={len(merged_lines)} "
        f"-> {output_path}"
    )