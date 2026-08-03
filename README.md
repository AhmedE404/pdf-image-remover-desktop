<div align="center">

# PDF Image Remover

[![Download Latest Release](https://img.shields.io/github/v/release/AhmedE404/pdf-image-remover-desktop?label=Download%20Latest%20Version&style=for-the-badge&color=success)](https://github.com/AhmedE404/pdf-image-remover-desktop/releases/latest)

A modern, fast, and user-friendly desktop application for removing repeated images (such as headers, footers, logos, or watermarks) from PDF files.

Built with **Python 3.10+**, **PyMuPDF**, and **PySide6**.

</div>

---

## Download

You don't need to install Python to use this app! You can download the ready-to-use executable for **Windows** or **macOS**:

👉 **[Go to the Releases Page to download the latest version](https://github.com/AhmedE404/pdf-image-remover-desktop/releases/latest)** 👈

*(If you are looking for installation instructions or how to bypass security warnings, please see the [Installation & Troubleshooting](#installation--troubleshooting) section below).*

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

## Running from Source

```bash
python main.py
```

---

## Installation & Troubleshooting

Because this is a free, open-source application, the compiled binaries are not signed with paid Developer Certificates ($99/yr for Apple, $300/yr for Windows EV). Therefore, your operating system might show a security warning. Here is how to safely bypass them:

### macOS ("App cannot be opened" or "Unverified Developer")
When you download the `.zip` release and extract the `.app`, macOS's Gatekeeper will block it from running by default. 

**Solution 1 (Settings):**
1. Try to open the app normally (it will be blocked).
2. Go to your Mac's **System Settings > Privacy & Security**.
3. Scroll down to the Security section. You will see a message saying "PDF Image Remover was blocked".
4. Click **Open Anyway** and confirm. The app will open and work forever.

**Solution 2 (Terminal - Recommended):**
To remove the Apple Quarantine flag completely, open your Terminal and run:
```bash
xattr -cr /path/to/PDF\ Image\ Remover.app
```
*(Tip: You can type `xattr -cr ` and just drag and drop the app into the terminal!)*

### Windows ("Windows protected your PC")
Because the application is not digitally signed with a paid certificate, Windows SmartScreen may block it.

* Whether you downloaded the **Portable (.exe)** or the **Standard (.zip)** version, click **More Info -> Run Anyway** when the blue screen appears.

---

## Project Structure

The project is organized into the following modules:

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

This project is released under the [MIT License](LICENSE).
