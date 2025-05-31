# main.py

from ocr.extract_text import extract_text_from_image, extract_text_from_pdf
from translate.translator import preserve_numbers_translate
from utils.file_loader import is_pdf, is_image
from config import LANGUAGES

def translate_payslip(file_path):
    if is_image(file_path):
        extracted_text = extract_text_from_image(file_path)
    elif is_pdf(file_path):
        extracted_text = extract_text_from_pdf(file_path)
    else:
        raise ValueError("Unsupported file format.")

    print("\n[Original Extracted Text]\n", extracted_text)

    for lang_code, lang_name in LANGUAGES.items():
        translated = preserve_numbers_translate(extracted_text, lang_code)
        print(f"\n[Translated to {lang_name}]\n{translated}")

if __name__ == "__main__":
    file_path = input("Enter the path to your payslip image or PDF: ")
    translate_payslip(file_path)
