# ocr/extract_text.py

import pytesseract
from pdf2image import convert_from_path
from PIL import Image
import cv2
import os

def extract_text_from_image(img_path):
    image = cv2.imread(img_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    text = pytesseract.image_to_string(gray)
    return text

def extract_text_from_pdf(pdf_path):
    pages = convert_from_path(pdf_path)
    text = ""
    for page in pages:
        temp_path = "temp_page.jpg"
        page.save(temp_path, "JPEG")
        text += extract_text_from_image(temp_path) + "\n"
        os.remove(temp_path)
    return text
