#!/usr/bin/env python3
"""Test that all required imports work correctly."""

try:
    import streamlit
    print("✓ Streamlit imported successfully")
except ImportError as e:
    print(f"✗ Failed to import streamlit: {e}")

try:
    import cv2
    print("✓ OpenCV imported successfully")
except ImportError as e:
    print(f"✗ Failed to import cv2: {e}")

try:
    import pytesseract
    print("✓ PyTesseract imported successfully")
except ImportError as e:
    print(f"✗ Failed to import pytesseract: {e}")

try:
    from utils.preprocessing import preprocess_image
    print("✓ Utils.preprocessing imported successfully")
except ImportError as e:
    print(f"✗ Failed to import utils.preprocessing: {e}")

try:
    from utils.ocr_extraction import extract_text_from_image
    print("✓ Utils.ocr_extraction imported successfully")
except ImportError as e:
    print(f"✗ Failed to import utils.ocr_extraction: {e}")

try:
    from utils.visualisation import visualise_text_regions
    print("✓ Utils.visualisation imported successfully")
except ImportError as e:
    print(f"✗ Failed to import utils.visualisation: {e}")

print("\nAll imports completed!")