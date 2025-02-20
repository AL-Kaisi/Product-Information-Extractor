# utils/ocr_extraction.py

import pytesseract
from PIL import Image
import re

def extract_text_from_image(image, regions):
    """
    Extract text from detected regions using OCR.
    """
    extracted_texts = []
    for (x, y, w, h) in regions:
        roi = image[y:y+h, x:x+w]
        text = pytesseract.image_to_string(roi, config="--psm 6").strip()
        if text:
            extracted_texts.append(text)
    return extracted_texts

def filter_text(extracted_texts):
    """
    Extract relevant product and retailer names from OCR results.
    """
    product_keywords = {"cleaner", "detergent", "disinfectant", "soda", "borax", "dishwasher"}
    retailer_keywords = {"atlas", "rayhong", "finish", "wrld", "walker"}

    product_names = []
    retailer_names = []

    for text in extracted_texts:
        # Ensure text is a string
        if isinstance(text, str):
            words = text.lower().split()
            if any(keyword in words for keyword in product_keywords):
                product_names.append(text)
            if any(keyword in words for keyword in retailer_keywords):
                retailer_names.append(text)

    return list(set(product_names)), list(set(retailer_names))
