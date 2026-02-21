import re
import os

try:
    import pytesseract
    from PIL import Image
    TESSERACT_AVAILABLE = True
    # Windows path — adjust if Tesseract installed elsewhere
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
except ImportError:
    TESSERACT_AVAILABLE = False

AADHAAR_PATTERN = re.compile(r'\b[2-9]\d{3}\s\d{4}\s\d{4}\b')
LICENSE_PATTERN  = re.compile(r'[A-Z]{2}[-\s]?\d{2}[-\s]?\d{4}[-\s]?\d{7}')


def extract_text_from_image(image_path):
    if not TESSERACT_AVAILABLE:
        return "", "OCR library not installed"
    try:
        img  = Image.open(image_path)
        text = pytesseract.image_to_string(img)
        return text, None
    except Exception as e:
        return "", str(e)


def extract_aadhaar_number(text):
    match = AADHAAR_PATTERN.search(text)
    return match.group(0).replace(' ', '') if match else ''


def extract_license_number(text):
    match = LICENSE_PATTERN.search(text)
    return match.group(0).replace(' ', '').replace('-', '') if match else ''


def process_document(ocr_doc_instance):
    """Process an OCRDocument instance, extract and save numbers."""
    from apps.driver.models import OCRDocument
    text, err = extract_text_from_image(ocr_doc_instance.image.path)
    ocr_doc_instance.extracted_text = text
    if ocr_doc_instance.document_type == 'aadhaar':
        ocr_doc_instance.extracted_number = extract_aadhaar_number(text)
    elif ocr_doc_instance.document_type == 'license':
        ocr_doc_instance.extracted_number = extract_license_number(text)
    ocr_doc_instance.save()
    return ocr_doc_instance.extracted_number
