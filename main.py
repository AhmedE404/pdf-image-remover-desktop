import sys
from PySide6.QtWidgets import QApplication, QDialog, QVBoxLayout, QLabel, QComboBox, QPushButton, QHBoxLayout
from PySide6.QtCore import Qt
from ui import PDFCleaner
from utils import translator

class LanguageDialog(QDialog):
    """
    First-launch dialog to ask the user for their preferred language.
    Changes text dynamically based on the selected combo box option.
    """
    def __init__(self):
        super().__init__()
        self.setFixedSize(350, 150)
        
        layout = QVBoxLayout()
        
        self.label = QLabel()
        self.label.setAlignment(Qt.AlignCenter)
        
        self.combo = QComboBox()
        for code, name in translator.get_available_languages():
            self.combo.addItem(name, code)
            
        self.combo.currentIndexChanged.connect(self.update_texts)
            
        btn_layout = QHBoxLayout()
        self.btn = QPushButton()
        self.btn.clicked.connect(self.accept)
        btn_layout.addStretch()
        btn_layout.addWidget(self.btn)
        btn_layout.addStretch()
        
        layout.addWidget(self.label)
        layout.addWidget(self.combo)
        layout.addLayout(btn_layout)
        self.setLayout(layout)
        
        # Initialize text based on the default item
        self.update_texts()
        
    def update_texts(self):
        lang_code = self.combo.currentData()
        
        self.setWindowTitle(translator.translate_for("dialog_title", lang_code))
        self.label.setText(translator.translate_for("dialog_label", lang_code))
        self.btn.setText(translator.translate_for("dialog_btn", lang_code))
        
        if translator.is_rtl(lang_code):
            self.setLayoutDirection(Qt.RightToLeft)
        else:
            self.setLayoutDirection(Qt.LeftToRight)

    def get_selected_language(self) -> str:
        return self.combo.currentData()

def main() -> None:
    """
    Application entry point.
    Initializes the Qt application, checks for first launch, and displays the main window.
    """
    app = QApplication(sys.argv)
    
    # Check if it's the first time the app is launched (no language saved)
    if not translator.has_saved_language():
        dialog = LanguageDialog()
        # If user clicks "Continue"
        if dialog.exec() == QDialog.Accepted:
            lang_code = dialog.get_selected_language()
            translator.set_language(lang_code)
        else:
            # If user closes the window without selecting, default to English
            translator.set_language("en")
            
    window = PDFCleaner()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()