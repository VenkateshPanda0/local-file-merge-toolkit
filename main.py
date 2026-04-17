"""
Local File Merge Toolkit
========================
A clean, modular CLI utility to merge PDF, PPTX, and text files locally.
No cloud upload. No GUI. Just clean, fast file merging.
"""

import os
import sys
import datetime

from utils.paths import (
    ensure_folders,
    get_files_in_folder,
    OUTPUT_DIR,
    sanitize_filename,
)

from utils.ui import (
    print_success,
    print_warning,
    print_error,
    prompt_menu,
)

from utils.hashing import calculate_sha256
from utils.validator import validate_files, validate_pdfs, validate_pptx

from modules.pdf_tools import merge_pdfs
from modules.ppt_tools import merge_pptx
from modules.text_tools import merge_text


# ---------------------------------------------------------
# Constants
# ---------------------------------------------------------

PDF_EXTS = [".pdf"]
PPTX_EXTS = [".pptx"]
TEXT_EXTS = [".txt", ".log", ".md"]


# ---------------------------------------------------------
# Helpers
# ---------------------------------------------------------

def auto_output_name(ext: str) -> str:
    """Generate automatic output filename."""
    ts = datetime.datetime.now().strftime("%Y_%m_%d_%H%M%S")
    return f"merged_{ts}{ext}"


def get_output_path(ext: str) -> str:
    """Prompt user for output filename."""
    raw = input("\nEnter output filename (leave blank for auto-generate): ").strip()

    if not raw:
        filename = auto_output_name(ext)
    else:
        filename = sanitize_filename(raw)

        if not filename.lower().endswith(ext):
            filename += ext

    return str(OUTPUT_DIR / filename)


def collect_files_manually(extensions: list[str]) -> list[str]:
    """Collect files one-by-one from user input."""
    print(f"\nSupported extensions: {', '.join(extensions)}")
    print("Enter file paths one by one.")
    print("Type 'done' when finished.\n")

    files = []

    while True:
        path = input("File path: ").strip().strip('"').strip("'")

        if path.lower() == "done":
            break

        if path:
            files.append(os.path.normpath(path))

    return files


def collect_files_from_folder(extensions: list[str]) -> list[str]:
    """Collect matching files from folder."""
    folder = input("Enter folder path: ").strip().strip('"').strip("'")
    folder = os.path.normpath(folder)

    files = get_files_in_folder(folder, extensions)

    if not files:
        print_warning("No matching files found (top-level folder only).")

    return files


def show_preview_and_confirm(files: list[str]) -> bool:
    """Show selected files and confirm."""
    print("\nSelected files:")

    for i, file in enumerate(files, 1):
        print(f"{i}. {os.path.basename(file)}")

    print(f"\nTotal files: {len(files)}")

    answer = input("Proceed? (Y/N): ").strip().lower()
    return answer in ("y", "yes")


def handle_selection(extensions: list[str]):
    """Choose manual or folder mode."""
    choice = prompt_menu(
        "Selection Method",
        {
            "1": "Select files manually",
            "2": "Merge all matching files in folder",
            "0": "Back",
        },
    )

    if choice == "0":
        return None

    if choice == "1":
        return collect_files_manually(extensions)

    return collect_files_from_folder(extensions)


def finalize_output(output_path: str) -> None:
    """Verify output and show hash."""
    if not os.path.exists(output_path):
        raise FileNotFoundError("Output file was not created.")

    hash_val = calculate_sha256(output_path)

    print_success("Done.")
    print_success(f"SHA256: {hash_val}")
    print_success(f"Saved to: {output_path}")


# ---------------------------------------------------------
# PDF Workflow
# ---------------------------------------------------------

def run_pdf_merge():
    files = handle_selection(PDF_EXTS)

    if files is None:
        return

    ok, result = validate_files(files, PDF_EXTS)
    if not ok:
        print_error(result)
        return

    ok, result = validate_pdfs(result)
    if not ok:
        print_error(result)
        return

    files = result

    if not show_preview_and_confirm(files):
        print_warning("Cancelled.")
        return

    output_path = get_output_path(".pdf")

    try:
        print("\nReading files...")
        print("Merging...")
        merge_pdfs(files, output_path)
        print("Saving...")
        finalize_output(output_path)

    except Exception as e:
        print_error(f"PDF merge failed: {e}")


# ---------------------------------------------------------
# PPTX Workflow
# ---------------------------------------------------------

def run_pptx_merge():
    files = handle_selection(PPTX_EXTS)

    if files is None:
        return

    ok, result = validate_files(files, PPTX_EXTS)
    if not ok:
        print_error(result)
        return

    ok, result = validate_pptx(result)
    if not ok:
        print_error(result)
        return

    files = result

    if not show_preview_and_confirm(files):
        print_warning("Cancelled.")
        return

    output_path = get_output_path(".pptx")

    try:
        print("\nReading files...")
        print("Merging...")
        merge_pptx(files, output_path)
        print("Saving...")
        finalize_output(output_path)

    except Exception as e:
        print_error(f"PPTX merge failed: {e}")


# ---------------------------------------------------------
# Text Workflow
# ---------------------------------------------------------

def run_text_merge():
    files = handle_selection(TEXT_EXTS)

    if files is None:
        return

    ok, result = validate_files(files, TEXT_EXTS)
    if not ok:
        print_error(result)
        return

    files = result

    if not show_preview_and_confirm(files):
        print_warning("Cancelled.")
        return

    separator = ""
    remove_duplicates = False
    sort_lines = False

    if input("\nAdd separator between files? (Y/N): ").strip().lower() in ("y", "yes"):
        separator = "=" * 40

    if input("Remove duplicate lines? (Y/N): ").strip().lower() in ("y", "yes"):
        remove_duplicates = True

    if input("Sort lines alphabetically? (Y/N): ").strip().lower() in ("y", "yes"):
        sort_lines = True

    if remove_duplicates and sort_lines:
    print_warning("Duplicate removal runs before sorting.")

    
    if sort_lines and separator:
        print_warning("Sorting enabled: separators will be omitted.")

    _, first_ext = os.path.splitext(files[0])
    output_ext = first_ext if first_ext in TEXT_EXTS else ".txt"

    output_path = get_output_path(output_ext)

    try:
        print("\nReading files...")
        print("Merging...")

        merge_text(
            files,
            output_path,
            separator=separator,
            remove_duplicates=remove_duplicates,
            sort_lines=sort_lines,
        )

        print("Saving...")
        finalize_output(output_path)

    except Exception as e:
        print_error(f"Text merge failed: {e}")


# ---------------------------------------------------------
# Main Menu
# ---------------------------------------------------------

def main():
    ensure_folders()

    while True:
        choice = prompt_menu(
            "Local File Merge Toolkit",
            {
                "1": "Merge PDF Files",
                "2": "Merge PPTX Files",
                "3": "Merge Text Files",
                "0": "Exit",
            },
        )

        if choice == "0":
            print_success("Goodbye!")
            sys.exit(0)

        elif choice == "1":
            run_pdf_merge()

        elif choice == "2":
            run_pptx_merge()

        elif choice == "3":
            run_text_merge()


if __name__ == "__main__":
    main()