import fitz
import tempfile
import os


def remove_image(pdf_path, output_path, xref, pages):

    doc = fitz.open(pdf_path)


    pix = fitz.Pixmap(
        fitz.csGRAY,
        fitz.IRect(0, 0, 1, 1),
        False
    )

    pix.clear_with(255)


    tmp = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".png"
    )

    pix.save(tmp.name)
    tmp.close()


    for page_number in pages:

        page = doc[page_number - 1]

        page.replace_image(
            xref,
            filename=tmp.name
        )


    doc.save(
        output_path,
        garbage=4,
        deflate=True
    )


    os.remove(tmp.name)
    doc.close()