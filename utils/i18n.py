from typing import Dict, Any, List, Tuple
from PySide6.QtCore import QSettings

TRANSLATIONS: Dict[str, Dict[str, Any]] = {
    "en": {
        "is_rtl": False,
        "lang_name": "English",
        "dialog_title": "Select Language",
        "dialog_label": "Welcome! Please select your preferred language:",
        "dialog_btn": "Continue",
        "window_title": "PDF Image Remover",
        "title_open": "Open a PDF file to begin\n(Or drag and drop here)",
        "title_scanning": "Scanning: {}",
        "title_select": "Select images to remove",
        "status_analyzing": "Analyzing PDF... Please wait.",
        "status_no_images": "No images found in this PDF.",
        "status_found": "Found {} unique image candidates.",
        "status_saving": "Saving PDF... This might take a while.",
        "status_saved": "✅ Finished successfully! PDF saved.",
        "status_error": "An error occurred: {}",
        "btn_settings": "Advanced Settings ⚙️",
        "grp_settings": "Advanced Settings",
        "lbl_garbage": "Garbage Collection Level:",
        "chk_deflate": "Compress File (Deflate)",
        "btn_open": "Open PDF",
        "btn_remove": "Remove Selected Images",
        "btn_remove_count": "Remove Selected Images ({})",
        "msg_error": "Error",
        "file_dialog_open": "Choose PDF",
        "file_dialog_save": "Save Cleaned PDF",
        "card_size": "Size:",
        "card_pages": "Pages:",
        "card_format": "Format:"
    },
    "ar": {
        "is_rtl": True,
        "lang_name": "العربية",
        "dialog_title": "اختر اللغة",
        "dialog_label": "مرحباً! الرجاء اختيار لغتك المفضلة:",
        "dialog_btn": "استمرار",
        "window_title": "مزيل الصور من الـ PDF",
        "title_open": "افتح ملف PDF للبدء\n(أو اسحب وأفلت الملف هنا)",
        "title_scanning": "جاري الفحص: {}",
        "title_select": "حدد الصور التي تريد إزالتها",
        "status_analyzing": "جاري تحليل الملف... يرجى الانتظار.",
        "status_no_images": "لم يتم العثور على أي صور في هذا الملف.",
        "status_found": "تم العثور على {} صور مختلفة.",
        "status_saving": "جاري الحفظ... قد يستغرق الأمر بعض الوقت.",
        "status_saved": "✅ تمت العملية بنجاح! تم حفظ الملف.",
        "status_error": "حدث خطأ: {}",
        "btn_settings": "إعدادات متقدمة ⚙️",
        "grp_settings": "إعدادات متقدمة",
        "lbl_garbage": "مستوى تنظيف الملف:",
        "chk_deflate": "ضغط مساحة الملف (Deflate)",
        "btn_open": "فتح ملف PDF",
        "btn_remove": "إزالة الصور المحددة",
        "btn_remove_count": "إزالة الصور المحددة ({})",
        "msg_error": "خطأ",
        "file_dialog_open": "اختر ملف PDF",
        "file_dialog_save": "حفظ ملف PDF المنظف",
        "card_size": "الأبعاد:",
        "card_pages": "الصفحات:",
        "card_format": "الصيغة:"
    },
    "eg": {
        "is_rtl": True,
        "lang_name": "مصرى 🇪🇬",
        "dialog_title": "اختار اللغة يا معلم",
        "dialog_label": "أهلاً بيك! نقي اللغة اللي تريحك:",
        "dialog_btn": "يلا بينا",
        "window_title": "شيل الصور من الـ PDF يا معلم",
        "title_open": "اختار ملف PDF عشان نبدأ\n(أو اسحبه وارميه هنا)",
        "title_scanning": "بندعبس جوا: {}",
        "title_select": "نقي الصور اللي عايز تطيرها",
        "status_analyzing": "بنفصص الملف... الصبر مفتاح الفرج.",
        "status_no_images": "الملف ده نضيف ومفيهوش ولا صورة.",
        "status_found": "لقينا {} صور مختلفة.",
        "status_saving": "بنحفظ الملف... أعمل كوباية شاي.",
        "status_saved": "✅ عظمة! الملف اتحفظ زي الفل.",
        "status_error": "يا ساتر يا رب! حصلت مشكلة: {}",
        "btn_settings": "الإعدادات والحبشتكنات ⚙️",
        "grp_settings": "تظبيط الشغل أهم من الشغل",
        "lbl_garbage": "مستوى تنضيف الكراكيب:",
        "chk_deflate": "اكبس مساحة الملف",
        "btn_open": "افتح ملف PDF",
        "btn_remove": "شيل الصور اللي اخترتها",
        "btn_remove_count": "شيل دول ({})",
        "msg_error": "حصل خير (خطأ)",
        "file_dialog_open": "اختار ملف الـ PDF",
        "file_dialog_save": "هتحفظ الملف الجديد فين؟",
        "card_size": "المقاس:",
        "card_pages": "موجودة في:",
        "card_format": "الصيغة:"
    }
}

class Translator:
    """Singleton translator class to manage current language and texts with persistence."""
    _instance = None
    
    def __new__(cls) -> 'Translator':
        if cls._instance is None:
            cls._instance = super(Translator, cls).__new__(cls)
            cls._instance.settings = QSettings("PyMuPDF_Tools", "PDFImageRemover")
            
            # Load saved language or default to 'en' if not set
            saved_lang = cls._instance.settings.value("language", None)
            if saved_lang and saved_lang in TRANSLATIONS:
                cls._instance.active_lang = saved_lang
            else:
                cls._instance.active_lang = "en"
                
        return cls._instance

    def has_saved_language(self) -> bool:
        """Checks if the user has explicitly chosen a language before."""
        return self.settings.contains("language")

    def set_language(self, lang_code: str) -> None:
        """Sets the active language code and saves it to QSettings."""
        if lang_code in TRANSLATIONS:
            self.active_lang = lang_code
            self.settings.setValue("language", lang_code)

    def get_language(self) -> str:
        """Returns the current active language code."""
        return self.active_lang
        
    def is_rtl(self, lang_code: str = None) -> bool:
        """Checks if a language is Right-To-Left (RTL). Uses active language if none provided."""
        code = lang_code if lang_code else self.active_lang
        return TRANSLATIONS.get(code, TRANSLATIONS["en"]).get("is_rtl", False)

    def get_available_languages(self) -> List[Tuple[str, str]]:
        """Returns a list of tuples containing (lang_code, lang_name) for UI dropdowns."""
        return [(code, data["lang_name"]) for code, data in TRANSLATIONS.items()]

    def translate_for(self, key: str, lang_code: str, *args: Any) -> str:
        """Translates a string for a SPECIFIC language (used in settings dialogs before applying)."""
        text = TRANSLATIONS.get(lang_code, TRANSLATIONS["en"]).get(key, key)
        if args:
            try:
                return text.format(*args)
            except Exception:
                return text
        return str(text)

    def translate(self, key: str, *args: Any) -> str:
        """
        Retrieves the translated string for a given key.
        Supports formatting with additional arguments.
        """
        return self.translate_for(key, self.active_lang, *args)

# Global instance for easy access across modules
translator = Translator()

def _t(key: str, *args: Any) -> str:
    """Helper function for quick translation."""
    return translator.translate(key, *args)
