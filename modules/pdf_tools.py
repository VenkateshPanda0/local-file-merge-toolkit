from pathlib import Path

from pypdf import PdfReader, PdfWriter
from pypdf.errors import PdfReadError

from utils.logger import log_action, log_failure
from utils.ui import print_warning


def merge_pdfs(
    file_list: list[str],
    output_path: str
) -> None:
    """
    Merge multiple PDF files into one output PDF.

    Skips:
    - encrypted PDFs
    - corrupt PDFs
    - unreadable PDFs
    - zero-page PDFs

    Raises error if no valid pages were merged.
    """

    writer = PdfWriter()

    successful_files = 0
    skipped_files = 0
    total_pages = 0

    for file_path in file_list:
        try:
            reader = PdfReader(file_path)

            # -------------------------------------------------
            # Encrypted PDF handling
            # -------------------------------------------------
            if reader.is_encrypted:
                try:
                    result = reader.decrypt("")

                    if result == 0:
                        msg = (
                            f"Encrypted PDF skipped "
                            f"(password required): {file_path}"
                        )
                        print_warning(msg)
                        log_failure(msg)
                        skipped_files += 1
                        continue

                except Exception:
                    msg = (
                        f"Encrypted PDF skipped "
                        f"(cannot decrypt): {file_path}"
                    )
                    print_warning(msg)
                    log_failure(msg)
                    skipped_files += 1
                    continue

            # -------------------------------------------------
            # Validate pages
            # -------------------------------------------------
            page_count = len(reader.pages)

            if page_count == 0:
                msg = f"Empty PDF skipped: {file_path}"
                print_warning(msg)
                log_failure(msg)
                skipped_files += 1
                continue

            # -------------------------------------------------
            # Add pages
            # -------------------------------------------------
            for page in reader.pages:
                writer.add_page(page)

            successful_files += 1
            total_pages += page_count

        except PdfReadError:
            msg = f"Invalid/corrupt PDF skipped: {file_path}"
            print_warning(msg)
            log_failure(msg)
            skipped_files += 1

        except Exception as e:
            msg = f"PDF skipped: {file_path} ({e})"
            print_warning(msg)
            log_failure(msg)
            skipped_files += 1

    # ---------------------------------------------------------
    # Prevent empty output
    # ---------------------------------------------------------
    if total_pages == 0:
        raise ValueError("No valid PDF pages found to merge.")

    # ---------------------------------------------------------
    # Ensure folder exists
    # ---------------------------------------------------------
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    # ---------------------------------------------------------
    # Save
    # ---------------------------------------------------------
    try:
        with open(output_path, "wb") as f:
            writer.write(f)

    except Exception as e:
        raise RuntimeError(f"Failed to save merged PDF: {e}")

    # ---------------------------------------------------------
    # Success Log
    # ---------------------------------------------------------
    log_action(
        "PDF merge success | "
        f"files_used={successful_files} "
        f"files_skipped={skipped_files} "
        f"pages={total_pages} "
        f"-> {output_path}"
    )