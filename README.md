# Local File Merge Toolkit

A modular Python command-line utility for merging files locally with a focus on reliability, clean architecture, and practical automation.

Designed as a lightweight productivity tool that processes files entirely on-device with no cloud dependency.

---

## Why This Project Matters

This project demonstrates practical software engineering skills beyond basic scripting:

- Modular project structure
- Input validation and defensive error handling
- File system operations and path safety
- Working with multiple real-world file formats
- Logging and auditability
- Data integrity verification using SHA256 hashing
- User-focused CLI design
- Maintainable and scalable code organization

---

## Core Features

## PDF Merge

- Merge multiple PDF files into one output document
- Preserves file order
- Automatically skips invalid, empty, encrypted, or unreadable PDFs
- Prevents blank output generation

## PPTX Merge

- Merge multiple PowerPoint presentations into one file
- Uses the first file as the base template/theme
- Copies slide content across presentations

> Best suited for standard text/image presentations.  
> Advanced animations, SmartArt, charts, media, or macros may have format limitations.

## Text Merge

Supports:

- `.txt`
- `.log`
- `.md`

Optional processing:

- Insert separators between merged files
- Remove duplicate lines
- Sort lines alphabetically
- Normalize output formatting

---

## Additional Engineering Features

- Colored interactive CLI interface using `colorama`
- SHA256 hash generation after successful output creation
- Persistent operation logs in `logs/history.log`
- Automatic folder creation (`output/`, `logs/`)
- Duplicate input filtering
- Graceful failure handling with informative messages

---

## Tech Stack

- Python 3.10+
- `pypdf`
- `python-pptx`
- `colorama`

---

## Project Structure

```text
local-file-merge-toolkit/
│── main.py
│── requirements.txt
│── modules/
│   ├── pdf_tools.py
│   ├── ppt_tools.py
│   └── text_tools.py
│── utils/
│   ├── hashing.py
│   ├── logger.py
│   ├── paths.py
│   ├── ui.py
│   └── validator.py
│── output/
│── logs/