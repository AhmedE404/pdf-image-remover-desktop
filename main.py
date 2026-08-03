import sys
import fitz

import tempfile
from pdf_engine import scan_pdf

from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QFileDialog,
    QProgressBar
)

from PySide6.QtGui import QPixmap
from PySide6.QtCore import (
    Qt,
    QThread,
    Signal
)


class ScanWorker(QThread):

    finished = Signal(list)

    def __init__(self, path):
        super().__init__()
        self.path = path

    def run(self):
        result = scan_pdf(self.path)
        self.finished.emit(result)



class SaveWorker(QThread):

    finished = Signal()

    def __init__(self, path, candidate, output):
        super().__init__()
        self.path = path
        self.candidate = candidate
        self.output = output


    def run(self):

        doc = fitz.open(self.path)

        pix = fitz.Pixmap(
            fitz.csGRAY,
            fitz.IRect(0,0,1,1),
            False
        )

        pix.clear_with(255)

        temp = tempfile.mktemp(suffix=".png")
        pix.save(temp)

        for page in self.candidate["pages"]:
            doc[page-1].replace_image(
                self.candidate["xref"],
                filename=temp
            )

        doc.save(
            self.output,
#             garbage=4,
            deflate=True
        )

        doc.close()

        self.finished.emit()



class PDFCleaner(QWidget):

    def __init__(self):

        super().__init__()

        self.setWindowTitle(
            "PDF Image Remover"
        )

        self.resize(
            750,
            700
        )


        self.pdf_path = None
        self.candidates = []
        self.current = 0


        self.title = QLabel(
            "Open PDF"
        )

        self.title.setAlignment(
            Qt.AlignCenter
        )


        self.status = QLabel()

        self.status.setAlignment(
            Qt.AlignCenter
        )


        self.image = QLabel()

        self.image.setFixedSize(
            500,
            400
        )

        self.image.setAlignment(
            Qt.AlignCenter
        )


        self.info = QLabel()

        self.info.setAlignment(
            Qt.AlignCenter
        )


        self.progress = QProgressBar()

        self.progress.hide()


        self.open_btn = QPushButton(
            "Open PDF"
        )

        self.open_btn.clicked.connect(
            self.open_pdf
        )


        self.remove_btn = QPushButton(
            "Remove Image"
        )

        self.remove_btn.clicked.connect(
            self.remove_image
        )


        self.next_btn = QPushButton(
            "Next Candidate"
        )

        self.next_btn.clicked.connect(
            self.next_candidate
        )


        box = QHBoxLayout()

        box.addWidget(
            self.remove_btn
        )

        box.addWidget(
            self.next_btn
        )


        layout = QVBoxLayout()

        layout.addWidget(
            self.title
        )

        layout.addWidget(
            self.image,
            alignment=Qt.AlignCenter
        )

        layout.addWidget(
            self.info
        )

        layout.addWidget(
            self.status
        )

        layout.addWidget(
            self.progress
        )

        layout.addWidget(
            self.open_btn
        )

        layout.addLayout(
            box
        )


        self.setLayout(
            layout
        )


        self.remove_btn.hide()
        self.next_btn.hide()



    def open_pdf(self):

        file,_ = QFileDialog.getOpenFileName(
            self,
            "Choose PDF",
            "",
            "PDF (*.pdf)"
        )

        if not file:
            return


        self.pdf_path = file

        self.title.setText(
            "Scanning..."
        )

        self.progress.show()

        self.progress.setRange(
            0,
            0
        )

        self.status.setText(
            "Analyzing PDF..."
        )


        self.worker = ScanWorker(
            file
        )

        self.worker.finished.connect(
            self.scan_done
        )

        self.worker.start()



    def scan_done(self,result):

        self.candidates = result

        self.progress.hide()

        if not result:
            self.status.setText(
                "No images found"
            )
            return


        self.current = 0

        self.remove_btn.show()
        self.next_btn.show()

        self.show_candidate()



    def show_candidate(self):

        c = self.candidates[self.current]


        pages = sorted(
            c["pages"]
        )


        self.title.setText(
            f"Candidate {self.current+1}/{len(self.candidates)}"
        )


        self.info.setText(
            f"""
Size: {c['width']} × {c['height']} px

Used:
{len(pages)} pages

Range:
{pages[0]} - {pages[-1]}

Format:
{c['ext']}
"""
        )


        doc = fitz.open(
            self.pdf_path
        )

        img = doc.extract_image(
            c["xref"]
        )

        pix = QPixmap()

        pix.loadFromData(
            img["image"]
        )


        pix = pix.scaled(
            450,
            350,
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )


        self.image.setPixmap(
            pix
        )

        doc.close()



    def next_candidate(self):

        self.current += 1

        if self.current >= len(self.candidates):
            self.current = 0

        self.show_candidate()



    def remove_image(self):

        out,_ = QFileDialog.getSaveFileName(
            self,
            "Save PDF",
            "",
            "PDF (*.pdf)"
        )


        if not out:
            return


        self.progress.show()

        self.progress.setRange(
            0,
            0
        )


        self.status.setText(
            "Saving PDF... Please wait"
        )


        self.save_worker = SaveWorker(
            self.pdf_path,
            self.candidates[self.current],
            out
        )


        self.save_worker.finished.connect(
            self.save_done
        )


        self.save_worker.start()



    def save_done(self):

        self.progress.hide()

        self.status.setText(
            "Finished"
        )



app = QApplication(sys.argv)

window = PDFCleaner()

window.show()

sys.exit(
    app.exec()
)