"""
CareerMatch AI — PDF Text Extractor
Extracts raw text from ATS-friendly PDF documents.
"""

from PyPDF2 import PdfReader


def extract_pdf_text(pdf_file):
    """
    Extract raw text from a PDF file with production-grade error handling.

    Args:
        pdf_file: File path (str) or file-like object (e.g., Streamlit UploadedFile).

    Returns:
        tuple: (extracted_text: str | None, status_message: str)
    """
    try:
        reader = PdfReader(pdf_file)
        raw_text = ""

        for page in reader.pages:
            extracted = page.extract_text()
            if extracted:
                raw_text += extracted + " "

        if not raw_text.strip():
            return None, "Document is empty or image-based (not ATS-friendly)."

        return raw_text.strip(), "Success"

    except Exception as e:
        return None, f"Failed to read PDF: {str(e)}"
