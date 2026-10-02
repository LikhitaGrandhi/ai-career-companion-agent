import fitz  # PyMuPDF
import pytesseract
from PIL import Image
from io import BytesIO


# Tesseract is installed here on Windows
pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)


def extract_text_from_pdf(file_path):

    doc = fitz.open(file_path)

    extracted_text = []

    for page in doc:

        # -------------------------------------------------
        # 1. Try normal PDF text extraction first
        # -------------------------------------------------
        text = page.get_text("text").strip()

        if text:
            extracted_text.append(text)

        # -------------------------------------------------
        # 2. If the page has little/no text, use OCR
        # -------------------------------------------------
        else:
            pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))

            image_bytes = pix.tobytes("png")

            image = Image.open(BytesIO(image_bytes))

            ocr_text = pytesseract.image_to_string(
                image,
                lang="eng"
            )

            if ocr_text.strip():
                extracted_text.append(ocr_text)

    return "\n".join(extracted_text)