import fitz
import tempfile
import os
from typing import List, Dict, Any

from PySide6.QtCore import QThread, Signal
from .engine import scan_pdf


class ScanWorker(QThread):
    """
    Background worker thread for scanning PDF files asynchronously.
    Prevents the main UI thread from freezing during long scans.
    """
    scan_completed = Signal(list)
    progress_update = Signal(int, int)
    error_occurred = Signal(str)

    def __init__(self, path: str):
        super().__init__()
        self.path = path

    def run(self) -> None:
        try:
            # Pass a local function to scan_pdf that emits the progress signals
            def progress_callback(page_number: int, total_pages: int) -> None:
                self.progress_update.emit(page_number, total_pages)

            result = scan_pdf(self.path, progress=progress_callback)
            self.scan_completed.emit(result)
            
        except Exception as e:
            self.error_occurred.emit(f"Failed to scan PDF: {str(e)}")


class SaveWorker(QThread):
    """
    Background worker thread for replacing selected images and saving the PDF.
    """
    save_completed = Signal()
    error_occurred = Signal(str)

    def __init__(self, path: str, selected_candidates: List[Dict[str, Any]], 
                 output: str, garbage_level: int, use_deflate: bool):
        super().__init__()
        self.path = path
        self.selected_candidates = selected_candidates
        self.output = output
        self.garbage_level = garbage_level
        self.use_deflate = use_deflate

    def run(self) -> None:
        try:
            doc = fitz.open(self.path)

            # Create a 1x1 transparent/white pixel
            pix = fitz.Pixmap(fitz.csGRAY, fitz.IRect(0, 0, 1, 1), False)
            pix.clear_with(255)

            # Save the dummy pixel to a secure temporary file
            tmp = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
            tmp_path = tmp.name
            
            try:
                pix.save(tmp_path)
                tmp.close()

                # Replace the target images with the dummy pixel across all relevant pages
                for candidate in self.selected_candidates:
                    for page_num in candidate["pages"]:
                        page = doc[page_num - 1]
                        page.replace_image(
                            candidate["xref"],
                            filename=tmp_path
                        )

                # Save the document with proper garbage collection and compression
                doc.save(
                    self.output,
                    garbage=self.garbage_level,
                    deflate=self.use_deflate
                )
            finally:
                # Securely remove the temporary file regardless of success or failure
                if os.path.exists(tmp_path):
                    os.remove(tmp_path)

            doc.close()
            self.save_completed.emit()
            
        except Exception as e:
            self.error_occurred.emit(str(e))
