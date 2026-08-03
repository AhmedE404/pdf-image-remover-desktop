import fitz
from typing import Dict, Any

from PySide6.QtWidgets import QFrame, QVBoxLayout, QLabel
from PySide6.QtGui import QPixmap, QCursor
from PySide6.QtCore import Qt, Signal

from utils import _t


class CandidateCard(QFrame):
    """
    UI Component representing a single image candidate in the grid.
    Supports selection toggling and dynamic translation.
    """
    selection_changed = Signal(bool)

    def __init__(self, candidate: Dict[str, Any], pdf_path: str):
        super().__init__()
        self.candidate = candidate
        self.pdf_path = pdf_path
        self.is_selected = False

        self.setFrameShape(QFrame.StyledPanel)
        self.setLineWidth(2)
        self.setCursor(QCursor(Qt.PointingHandCursor))

        self.update_style()

        layout = QVBoxLayout()
        
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        
        self.info_label = QLabel()
        self.info_label.setAlignment(Qt.AlignCenter)
        
        layout.addWidget(self.image_label)
        layout.addWidget(self.info_label)
        self.setLayout(layout)
        
        self.load_image()
        self.retranslate_ui()

    def retranslate_ui(self) -> None:
        """Updates the text based on the active language."""
        pages = sorted(self.candidate["pages"])
        self.info_label.setText(
            f"{_t('card_size')} {self.candidate['width']}x{self.candidate['height']} px\n"
            f"{_t('card_pages')} {len(pages)} | {_t('card_format')} {self.candidate['ext']}"
        )

    def update_style(self) -> None:
        """Updates the visual style of the card based on its selection state."""
        if self.is_selected:
            self.setStyleSheet("""
                CandidateCard {
                    border: 2px solid #0078D7;
                    background-color: rgba(0, 120, 215, 0.1);
                    border-radius: 5px;
                }
            """)
        else:
            self.setStyleSheet("""
                CandidateCard {
                    border: 1px solid #CCC;
                    background-color: transparent;
                    border-radius: 5px;
                }
                CandidateCard:hover {
                    border: 1px solid #888;
                }
            """)

    def load_image(self) -> None:
        """Loads and scales the image from the PDF safely."""
        doc = fitz.open(self.pdf_path)
        try:
            img = doc.extract_image(self.candidate["xref"])
            pix = QPixmap()
            pix.loadFromData(img["image"])
            pix = pix.scaled(
                200, 200,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            self.image_label.setPixmap(pix)
        except Exception:
            self.image_label.setText("Error")
        finally:
            doc.close()

    def mousePressEvent(self, event) -> None:
        """Handles mouse clicks for toggling selection."""
        if event.button() == Qt.LeftButton:
            self.is_selected = not self.is_selected
            self.update_style()
            self.selection_changed.emit(self.is_selected)
