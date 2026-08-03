import fitz
import hashlib
import math


def scan_pdf(path, progress=None):

    doc = fitz.open(path)

    images = {}

    total_pages = len(doc)


    for page_number, page in enumerate(doc, start=1):

        if progress:
            progress(
                page_number,
                total_pages
            )


        for xref, *_ in page.get_images(full=True):

            try:
                data = doc.extract_image(xref)

            except Exception:
                continue


            image_hash = hashlib.md5(
                data["image"]
            ).hexdigest()


            if image_hash not in images:

                images[image_hash] = {
                    "xref": xref,
                    "width": data["width"],
                    "height": data["height"],
                    "ext": data["ext"],
                    "pages": set()
                }


            images[image_hash]["pages"].add(
                page_number
            )


    doc.close()


    candidates = list(
        images.values()
    )


    candidates.sort(
        key=lambda x:
            len(x["pages"]) * 100
            +
            math.log(
                x["width"] * x["height"],
                2
            ),
        reverse=True
    )


    return candidates