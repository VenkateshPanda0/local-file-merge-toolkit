import os


def validate_files(
    file_list: list[str],
    extensions: list[str]
) -> tuple[bool, list[str] | str]:
    """
    Validate generic files.

    Checks:
    - at least 2 selected
    - exists
    - is file
    - readable
    - allowed extension
    - removes duplicates
    """

    if len(file_list) < 2:
        return False, "At least 2 files must be selected."

    errors = []
    valid_files = []
    seen = set()

    for raw_path in file_list:
        path = os.path.normpath(raw_path)

        if path in seen:
            continue

        seen.add(path)

        if not os.path.exists(path):
            errors.append(f"Missing: {path}")
            continue

        if not os.path.isfile(path):
            errors.append(f"Not a file: {path}")
            continue

        if not os.access(path, os.R_OK):
            errors.append(f"Unreadable: {path}")
            continue

        _, ext = os.path.splitext(path)

        if ext.lower() not in extensions:
            errors.append(
                f"Invalid extension: {path} "
                f"(allowed: {', '.join(extensions)})"
            )
            continue

        valid_files.append(path)

    if len(valid_files) < 2:
        msg = "Need at least 2 valid files."
        if errors:
            msg += "\n" + "\n".join(errors)
        return False, msg

    return True, valid_files


# ---------------------------------------------------------
# PDF Validation
# ---------------------------------------------------------

def validate_pdfs(
    file_list: list[str]
) -> tuple[bool, list[str] | str]:
    """
    Validate PDFs.

    Skips:
    - encrypted PDFs
    - corrupt PDFs

    Requires at least 2 valid files.
    """

    try:
        from pypdf import PdfReader
    except ImportError:
        return False, "pypdf library is not installed."

    valid_files = []
    errors = []

    for path in file_list:
        try:
            reader = PdfReader(path)

            if reader.is_encrypted:
                errors.append(f"Encrypted PDF skipped: {path}")
                continue

            _ = len(reader.pages)
            valid_files.append(path)

        except Exception:
            errors.append(f"Invalid/corrupt PDF skipped: {path}")

    if len(valid_files) < 2:
        msg = "Need at least 2 valid PDF files."
        if errors:
            msg += "\n" + "\n".join(errors)
        return False, msg

    return True, valid_files


# ---------------------------------------------------------
# PPTX Validation
# ---------------------------------------------------------

def validate_pptx(
    file_list: list[str]
) -> tuple[bool, list[str] | str]:
    """
    Validate PPTX files.

    Skips corrupt files.
    Requires at least 2 valid files.
    """

    try:
        from pptx import Presentation
    except ImportError:
        return False, "python-pptx library is not installed."

    valid_files = []
    errors = []

    for path in file_list:
        try:
            _ = Presentation(path)
            valid_files.append(path)

        except Exception:
            errors.append(f"Invalid/corrupt PPTX skipped: {path}")

    if len(valid_files) < 2:
        msg = "Need at least 2 valid PPTX files."
        if errors:
            msg += "\n" + "\n".join(errors)
        return False, msg

    return True, valid_files