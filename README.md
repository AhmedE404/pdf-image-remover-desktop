# PDF Image Remover

A modern, fast, and user-friendly desktop application for removing repeated images (such as headers, footers, logos, or watermarks) from PDF files.

Built with:
* **Python 3.10+**
* **PyMuPDF** (for fast PDF manipulation)
* **PySide6** (for a modern GUI)

---

## Features

* **Drag & Drop**: Easily drop a PDF into the window to start scanning immediately.
* **Smart Detection**: Automatically detect identical repeated images using MD5 hashing.
* **Visual Selection**: Preview all image candidates in a responsive grid before taking action.
* **Multi-Selection**: Select and remove multiple different watermarks/images at once.
* **Advanced Settings**: Control PyMuPDF's garbage collection levels and Deflate compression to balance speed and file size.
* **Bilingual Support (i18n)**: Fully supports English and Arabic (with dynamic RTL/LTR layout switching).
* **Asynchronous Processing**: Background workers ensure the UI never freezes during heavy PDF operations.

---

## Requirements

* Python 3.10+
* PyMuPDF
* PySide6

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Run

```bash
python main.py
```

---

## Project Architecture (Clean Code)

The project follows a clean, enterprise-grade modular architecture:

```
.
├── core/
│   ├── engine.py       # PDF parsing and image hashing algorithms
│   └── workers.py      # QThread background workers
├── ui/
│   ├── main_window.py  # Main PDFCleaner application window
│   └── components.py   # Reusable UI widgets (e.g., CandidateCard)
├── utils/
│   └── i18n.py         # Singleton translation manager and QSettings persistence
├── main.py             # Application entry point
├── requirements.txt
└── README.md
```

---

## Build Executable

Building the standalone application is now fully automated and cross-platform.

```bash
python build_app.py
```

This script will automatically detect whether you are on Windows or macOS, install the necessary dependencies (like `pyinstaller`), apply the correct OS-specific flags, and generate a single executable file in the `dist/` directory.

---

## License

This project is released under the MIT License.
