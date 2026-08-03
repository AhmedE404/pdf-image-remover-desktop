import fitz
import hashlib
import math
from typing import Callable, List, Dict, Any, Optional

def scan_pdf(path: str, progress: Optional[Callable[[int, int], None]] = None) -> List[Dict[str, Any]]:
    """
    Scans a PDF file to detect and extract identical repeated images.
    
    Args:
        path (str): The absolute or relative path to the PDF file.
        progress (Optional[Callable[[int, int], None]]): A callback function that 
            receives (current_page, total_pages) to track scan progress.
            
    Returns:
        List[Dict[str, Any]]: A sorted list of dictionaries representing image candidates.
        Each candidate dictionary contains:
            - 'xref' (int): The image object reference ID in the PDF.
            - 'width' (int): Image width in pixels.
            - 'height' (int): Image height in pixels.
            - 'ext' (str): Image extension (e.g., 'jpeg', 'png').
            - 'pages' (Set[int]): A set of page numbers where this image appears.
    """
    doc = fitz.open(path)
    images: Dict[str, Dict[str, Any]] = {}
    total_pages = len(doc)

    for page_number, page in enumerate(doc, start=1):
        if progress:
            progress(page_number, total_pages)

        # full=True ensures we get the most detailed image blocks
        for xref, *_ in page.get_images(full=True):
            try:
                data = doc.extract_image(xref)
                if not data or "image" not in data:
                    continue
                # Group identical images using MD5 hash of their binary data
                image_hash = hashlib.md5(data["image"]).hexdigest()
            except Exception:
                continue

            if image_hash not in images:
                images[image_hash] = {
                    "xref": xref,
                    "width": data.get("width", 0),
                    "height": data.get("height", 0),
                    "ext": data.get("ext", ""),
                    "pages": set()
                }

            images[image_hash]["pages"].add(page_number)

    doc.close()

    # Convert the dictionary to a list of candidates
    candidates = list(images.values())

    # Sort candidates based on an algorithmic score:
    # 1. Number of times it appears (weight: 100)
    # 2. Image resolution (using Log2 to normalize large dimensions)
    candidates.sort(
        key=lambda x: len(x["pages"]) * 100 + math.log(max(1, x["width"] * x["height"]), 2),
        reverse=True
    )

    return candidates
