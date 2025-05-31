# utils/file_loader.py

import os

def is_pdf(file_path):
    return file_path.lower().endswith('.pdf')

def is_image(file_path):
    return any(file_path.lower().endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.bmp'])
