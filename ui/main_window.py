import os
from typing import List, Dict, Any

from PySide6.QtWidgets import (
    QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout,
    QFileDialog, QProgressBar, QScrollArea, QGridLayout,
    QMessageBox, QComboBox, QGroupBox, QFormLayout, QCheckBox
)
from PySide6.QtGui import QCursor, QDragEnterEvent, QDropEvent
from PySide6.QtCore import Qt

from core.workers import ScanWorker, SaveWorker
from ui.components import CandidateCard
from utils import _t, translator


class PDFCleaner(QWidget):
    """
    Main application window.
    Handles the UI layout, drag & drop, and orchestration of background workers.
    """
    def __init__(self):
        super().__init__()
        self.resize(850, 750)
        self.setAcceptDrops(True)

        self.pdf_path: str | None = None
        self.candidates: List[Dict[str, Any]] = []
        self.cards: List[CandidateCard] = []

        self.setup_ui()
        self.retranslate_ui()

    def setup_ui(self) -> None:
        """Initializes and arranges all UI widgets."""
        
        # Language Selection ComboBox
        self.lang_combo = QComboBox()
        self.lang_combo.setCursor(QCursor(Qt.PointingHandCursor))
        
        # Populate languages
        for code, name in translator.get_available_languages():
            self.lang_combo.addItem(name, code)
            
        # Set current index to active language
        current_lang = translator.get_language()
        index = self.lang_combo.findData(current_lang)
        if index >= 0:
            self.lang_combo.setCurrentIndex(index)
            
        self.lang_combo.currentIndexChanged.connect(self.change_language)
        
        self.title = QLabel()
        self.title.setAlignment(Qt.AlignCenter)
        font = self.title.font()
        font.setPointSize(18)
        font.setBold(True)
        self.title.setFont(font)
        self.title.setStyleSheet("margin: 10px 0;")

        self.status = QLabel()
        self.status.setAlignment(Qt.AlignCenter)
        self.status.setStyleSheet("font-weight: bold; margin: 10px 0;")

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_widget = QWidget()
        self.grid_layout = QGridLayout(self.scroll_widget)
        self.grid_layout.setSpacing(15)
        self.grid_layout.setContentsMargins(15, 15, 15, 15)
        self.scroll_area.setWidget(self.scroll_widget)
        
        self.progress = QProgressBar()
        self.progress.hide()

        self.settings_btn = QPushButton()
        self.settings_btn.setFlat(True)
        self.settings_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.settings_btn.clicked.connect(self.toggle_settings)
        self.settings_btn.setStyleSheet("border: none; background: transparent; color: #555; text-decoration: underline;")
        
        self.settings_group = QGroupBox()
        self.settings_group.hide()
        form_layout = QFormLayout()
        
        self.garbage_lbl = QLabel()
        self.garbage_combo = QComboBox()
        self.garbage_combo.addItem("None (0)", 0)
        self.garbage_combo.addItem("Fast (1)", 1)
        self.garbage_combo.addItem("Default (2)", 2)
        self.garbage_combo.addItem("Thorough (3)", 3)
        self.garbage_combo.addItem("Extreme (4)", 4)
        self.garbage_combo.setCurrentIndex(2)
        
        self.deflate_chk = QCheckBox()
        self.deflate_chk.setChecked(True)

        form_layout.addRow(self.garbage_lbl, self.garbage_combo)
        form_layout.addRow(self.deflate_chk)
        self.settings_group.setLayout(form_layout)

        self.open_btn = QPushButton()
        self.open_btn.setMinimumHeight(45)
        self.open_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.open_btn.clicked.connect(self.open_pdf_dialog)
        self.open_btn.setDefault(True) # Make Open default initially

        self.remove_btn = QPushButton()
        self.remove_btn.setMinimumHeight(45)
        self.remove_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.remove_btn.setEnabled(False)
        self.remove_btn.clicked.connect(self.remove_images)

        top_layout = QHBoxLayout()
        top_layout.addStretch()
        top_layout.addWidget(self.lang_combo)

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)
        layout.addLayout(top_layout)
        layout.addWidget(self.title)
        layout.addWidget(self.scroll_area, stretch=1)
        
        settings_layout = QHBoxLayout()
        settings_layout.addStretch()
        settings_layout.addWidget(self.settings_btn)
        
        layout.addLayout(settings_layout)
        layout.addWidget(self.settings_group)
        layout.addWidget(self.status)
        layout.addWidget(self.progress)
        
        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.open_btn)
        btn_layout.addWidget(self.remove_btn)
        
        layout.addLayout(btn_layout)
        self.setLayout(layout)

    def retranslate_ui(self) -> None:
        """Applies the current language translations to all UI elements."""
        self.setWindowTitle(_t("window_title"))
        
        if not self.pdf_path:
            self.title.setText(_t("title_open"))
        elif not self.candidates:
            self.title.setText(_t("title_scanning", os.path.basename(self.pdf_path)))
        else:
            self.title.setText(_t("title_select"))
            
        self.settings_btn.setText(_t("btn_settings"))
        self.settings_group.setTitle(_t("grp_settings"))
        
        self.garbage_lbl.setText(_t("lbl_garbage"))
        self.deflate_chk.setText(_t("chk_deflate"))

        self.open_btn.setText(_t("btn_open"))
        self.check_selections()

        for card in self.cards:
            card.retranslate_ui()

        # Update RTL/LTR layout direction
        if translator.is_rtl():
            self.setLayoutDirection(Qt.RightToLeft)
        else:
            self.setLayoutDirection(Qt.LeftToRight)

    def change_language(self, index: int) -> None:
        """Handles user changing language from the combo box."""
        lang_code = self.lang_combo.itemData(index)
        if lang_code:
            translator.set_language(lang_code)
            self.retranslate_ui()

    def toggle_settings(self) -> None:
        """Shows or hides the advanced settings panel."""
        self.settings_group.setVisible(self.settings_group.isHidden())

    def clear_grid(self) -> None:
        """Clears all CandidateCards from the UI grid."""
        for i in reversed(range(self.grid_layout.count())): 
            widget = self.grid_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)
                widget.deleteLater()
        self.cards.clear()
        self.check_selections()

    def dragEnterEvent(self, event: QDragEnterEvent) -> None:
        """Accepts file drag events if the file is a PDF and no task is running."""
        if not self.open_btn.isEnabled():
            event.ignore()
            return
            
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            if urls and urls[0].toLocalFile().lower().endswith('.pdf'):
                event.acceptProposedAction()
                return
        event.ignore()

    def dropEvent(self, event: QDropEvent) -> None:
        """Handles dropped PDF files."""
        if not self.open_btn.isEnabled():
            return
            
        urls = event.mimeData().urls()
        if urls:
            file_path = urls[0].toLocalFile()
            if file_path.lower().endswith('.pdf'):
                self.start_scan(file_path)

    def open_pdf_dialog(self) -> None:
        """Opens a file dialog for the user to select a PDF."""
        file, _ = QFileDialog.getOpenFileName(
            self, _t("file_dialog_open"), "", "PDF (*.pdf)"
        )
        if file:
            self.start_scan(file)

    def start_scan(self, file_path: str) -> None:
        """Initiates the scanning process for the selected PDF."""
        self.pdf_path = file_path
        self.clear_grid()
        self.title.setText(_t("title_scanning", os.path.basename(file_path)))
        
        self.progress.show()
        self.progress.setRange(0, 100)
        self.progress.setValue(0)
        
        self.status.setStyleSheet("color: black; font-weight: bold;")
        self.status.setText(_t("status_analyzing"))
        
        self.open_btn.setEnabled(False)
        self.remove_btn.setEnabled(False)
        self.open_btn.setDefault(False)

        self.worker = ScanWorker(file_path)
        self.worker.progress_update.connect(self.update_scan_progress)
        self.worker.scan_completed.connect(self.scan_done)
        self.worker.error_occurred.connect(self.handle_error)
        self.worker.start()

    def update_scan_progress(self, current: int, total: int) -> None:
        """Updates the progress bar during PDF scanning."""
        if total > 0:
            val = int((current / total) * 100)
            self.progress.setValue(val)

    def scan_done(self, result: List[Dict[str, Any]]) -> None:
        """Handles the completion of the PDF scan."""
        self.progress.hide()
        self.open_btn.setEnabled(True)

        self.candidates = result
        if not result:
            self.status.setStyleSheet("color: #D32F2F; font-weight: bold;")
            self.status.setText(_t("status_no_images"))
            self.title.setText(_t("title_open"))
            self.open_btn.setDefault(True) # Make Open default again
            return

        self.status.setStyleSheet("color: black; font-weight: bold;")
        self.status.setText(_t("status_found", len(result)))
        self.title.setText(_t("title_select"))
        self.populate_grid()

    def handle_error(self, message: str) -> None:
        """Displays error messages gracefully and resets UI state."""
        self.progress.hide()
        self.open_btn.setEnabled(True)
        
        # Re-enable cards in case they were disabled during a save attempt
        for card in self.cards:
            card.setEnabled(True)
            
        self.check_selections()
        self.status.setStyleSheet("color: #D32F2F; font-weight: bold;")
        self.status.setText(_t("status_error", message))
        
        QMessageBox.critical(self, _t("msg_error"), message)

    def populate_grid(self) -> None:
        """Populates the UI grid with CandidateCards."""
        columns = 3
        for index, candidate in enumerate(self.candidates):
            card = CandidateCard(candidate, self.pdf_path)
            card.selection_changed.connect(self.check_selections)
            self.cards.append(card)
            
            row = index // columns
            col = index % columns
            self.grid_layout.addWidget(card, row, col)

    def check_selections(self) -> None:
        """Updates the remove button state based on selected cards."""
        selected_count = sum(1 for card in self.cards if card.is_selected)
        has_selection = selected_count > 0
        
        self.remove_btn.setEnabled(has_selection)
        
        # If an image is selected, make Remove button the Default (Enter key triggers it)
        self.remove_btn.setDefault(has_selection)
        # If no image is selected, make Open button the Default
        self.open_btn.setDefault(not has_selection)
        
        if has_selection:
            self.remove_btn.setText(_t("btn_remove_count", selected_count))
        else:
            self.remove_btn.setText(_t("btn_remove"))

    def get_selected_candidates(self) -> List[Dict[str, Any]]:
        """Returns a list of data for all currently selected CandidateCards."""
        return [card.candidate for card in self.cards if card.is_selected]

    def remove_images(self) -> None:
        """Initiates the background process to remove selected images and save the PDF."""
        selected = self.get_selected_candidates()
        if not selected:
            return

        out, _ = QFileDialog.getSaveFileName(
            self, _t("file_dialog_save"), "", "PDF (*.pdf)"
        )

        if not out:
            return

        self.progress.show()
        self.progress.setRange(0, 0)
        
        self.status.setStyleSheet("color: black; font-weight: bold;")
        self.status.setText(_t("status_saving"))
        
        self.open_btn.setEnabled(False)
        self.remove_btn.setEnabled(False)
        for card in self.cards:
            card.setEnabled(False)

        garbage_val = self.garbage_combo.currentData()
        use_deflate = self.deflate_chk.isChecked()

        self.save_worker = SaveWorker(self.pdf_path, selected, out, garbage_val, use_deflate)
        self.save_worker.save_completed.connect(self.save_done)
        self.save_worker.error_occurred.connect(self.handle_error)
        self.save_worker.start()

    def save_done(self) -> None:
        """Handles the completion of the PDF saving process."""
        self.progress.hide()
        
        self.status.setStyleSheet("color: #2E7D32; font-weight: bold; font-size: 14px;")
        self.status.setText(_t("status_saved"))
        
        self.open_btn.setEnabled(True)
        for card in self.cards:
            card.setEnabled(True)
        self.check_selections()
