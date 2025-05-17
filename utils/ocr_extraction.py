# utils/ocr_extraction.py

import pytesseract
from PIL import Image
import re
import cv2
import numpy as np
from typing import List, Tuple, Dict, Optional
from config import Config

def enhance_image_for_ocr(image: np.ndarray) -> np.ndarray:
    """
    Apply additional image enhancement techniques for better OCR results.
    """
    # Convert to greyscale if not already
    if len(image.shape) == 3:
        grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        grey = image.copy()
    
    # Denoise
    denoised = cv2.fastNlMeansDenoising(grey)
    
    # Apply CLAHE (Contrast Limited Adaptive Histogram Equalisation)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    enhanced = clahe.apply(denoised)
    
    # Sharpen the image
    kernel = np.array([[-1,-1,-1],
                      [-1, 9,-1],
                      [-1,-1,-1]])
    sharpened = cv2.filter2D(enhanced, -1, kernel)
    
    # Apply binary threshold
    _, binary = cv2.threshold(sharpened, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    # Resize if too small
    height, width = binary.shape
    if height < 50 or width < 50:
        scale_factor = max(50/height, 50/width)
        new_width = int(width * scale_factor)
        new_height = int(height * scale_factor)
        binary = cv2.resize(binary, (new_width, new_height), interpolation=cv2.INTER_CUBIC)
    
    return binary

def preprocess_for_text_detection(image: np.ndarray) -> np.ndarray:
    """
    Preprocess image specifically for text detection.
    """
    # Convert to greyscale
    grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply bilateral filter to reduce noise while keeping edges sharp
    filtered = cv2.bilateralFilter(grey, 11, 17, 17)
    
    # Apply CLAHE for better contrast
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    enhanced = clahe.apply(filtered)
    
    # Edge detection
    edges = cv2.Canny(enhanced, 30, 200)
    
    # Dilate to connect text regions
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
    dilated = cv2.dilate(edges, kernel, iterations=1)
    
    # Find contours
    contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Create mask for text regions
    mask = np.zeros_like(grey)
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 100:  # Filter small contours
            cv2.drawContours(mask, [contour], -1, 255, -1)
    
    # Apply mask to original image
    result = cv2.bitwise_and(enhanced, enhanced, mask=mask)
    
    return result

def extract_text_with_confidence(image: np.ndarray, config_string: str = "--psm 3") -> Tuple[str, float]:
    """
    Extract text from image with confidence score.
    """
    try:
        # Get detailed OCR data
        data = pytesseract.image_to_data(image, config=config_string, output_type=pytesseract.Output.DICT)
        
        # Extract text with confidence
        texts = []
        confidences = []
        
        for i in range(len(data['text'])):
            if int(data['conf'][i]) > 0:  # Only consider text with positive confidence
                text = data['text'][i].strip()
                conf = float(data['conf'][i])
                if text and len(text) > 1:  # Filter out single characters
                    texts.append(text)
                    confidences.append(conf)
        
        if texts:
            # Join the texts and calculate average confidence
            full_text = ' '.join(texts)
            avg_confidence = np.mean(confidences) if confidences else 0
            return full_text, avg_confidence
        
    except Exception as e:
        print(f"OCR error: {e}")
    
    return "", 0.0

def extract_text_from_image(image: np.ndarray, regions: List[Tuple[int, int, int, int]]) -> Tuple[List[str], List[float]]:
    """
    Extract text from detected regions using multiple OCR strategies.
    """
    extracted_texts = []
    confidence_scores = []
    
    # Try full image OCR first
    full_image_preprocessed = preprocess_for_text_detection(image)
    full_text, full_confidence = extract_text_with_confidence(full_image_preprocessed, "--psm 3")
    
    if full_text and full_confidence > 50:
        extracted_texts.append(full_text)
        confidence_scores.append(full_confidence)
    
    # Process individual regions
    for (x, y, w, h) in regions:
        # Skip very small regions
        if w < 20 or h < 20:
            continue
            
        # Add padding to the region for better OCR
        padding = 10
        x_start = max(0, x - padding)
        y_start = max(0, y - padding)
        x_end = min(image.shape[1], x + w + padding)
        y_end = min(image.shape[0], y + h + padding)
        
        roi = image[y_start:y_end, x_start:x_end]
        
        # Try multiple preprocessing techniques
        preprocessing_methods = [
            lambda img: enhance_image_for_ocr(img),
            lambda img: cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) if len(img.shape) == 3 else img,
            lambda img: preprocess_for_text_detection(img)
        ]
        
        best_text = ""
        best_confidence = 0
        
        for preprocess_func in preprocessing_methods:
            try:
                processed_roi = preprocess_func(roi)
                
                # Try multiple PSM modes
                psm_modes = [6, 8, 7, 11, 13]  # Different OCR modes
                
                for psm in psm_modes:
                    text, confidence = extract_text_with_confidence(
                        processed_roi, 
                        f"--psm {psm} -l eng"
                    )
                    
                    if confidence > best_confidence and len(text) > 2:
                        best_text = text
                        best_confidence = confidence
                        
            except Exception as e:
                continue
        
        if best_text and best_confidence > 30:
            extracted_texts.append(best_text)
            confidence_scores.append(best_confidence)
    
    # Remove duplicates while preserving order
    unique_texts = []
    unique_scores = []
    seen = set()
    
    for text, score in zip(extracted_texts, confidence_scores):
        text_lower = text.lower().strip()
        if text_lower not in seen and len(text_lower) > 2:
            seen.add(text_lower)
            unique_texts.append(text)
            unique_scores.append(score)
    
    return unique_texts, unique_scores

def extract_patterns(text: str) -> Dict[str, List[str]]:
    """
    Extract common patterns from text using regex.
    """
    patterns = {
        'prices': r'[$£€]\s*\d+(?:[.,]\d{2})?|\d+(?:[.,]\d{2})?\s*[$£€]',
        'dates': r'\d{1,2}[-/]\d{1,2}[-/]\d{2,4}|(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{1,2},?\s+\d{2,4}',
        'percentages': r'\d+\.?\d*\s*%',
        'weights': r'\d+\.?\d*\s*(?:kg|g|mg|lb|oz|lbs|ounces?)\b',
        'volumes': r'\d+\.?\d*\s*(?:ml|l|L|mL|gal|gallons?|fl\.?\s*oz)\b',
        'product_codes': r'\b[A-Z]{2,}\d{3,}|\d{3,}[A-Z]{2,}\b|UPC\s*:\s*\d+',
        'barcodes': r'\b\d{8,13}\b',
        'expiry': r'(?:exp|expiry|expires?|best\s+before)[:\s]*[\d/\-\s]+\d{2,4}',
    }
    
    results = {}
    for pattern_name, pattern in patterns.items():
        matches = re.findall(pattern, text, re.IGNORECASE)
        results[pattern_name] = matches
    
    return results

def filter_text(extracted_texts: List[str], confidence_scores: List[float], min_confidence: float = 30.0) -> Dict[str, List[str]]:
    """
    Enhanced text filtering with confidence scores and pattern extraction.
    """
    # Get keywords from config
    product_keywords = Config.KEYWORDS['product_keywords']
    retailer_keywords = Config.KEYWORDS['retailer_keywords']
    brand_keywords = Config.KEYWORDS['brand_keywords']
    
    product_names = []
    retailer_names = []
    brand_names = []
    prices = []
    dates = []
    weights = []
    volumes = []
    percentages = []
    other_details = []
    
    # Clean and process texts
    for text, confidence in zip(extracted_texts, confidence_scores):
        # Skip low confidence text and very short text
        if confidence < min_confidence or len(text.strip()) < 3:
            continue
        
        # Clean text
        cleaned_text = ' '.join(text.split())  # Remove extra whitespace
        
        # Extract patterns from text
        patterns = extract_patterns(cleaned_text)
        
        # Add extracted patterns to results
        prices.extend(patterns.get('prices', []))
        dates.extend(patterns.get('dates', []))
        dates.extend(patterns.get('expiry', []))
        weights.extend(patterns.get('weights', []))
        volumes.extend(patterns.get('volumes', []))
        percentages.extend(patterns.get('percentages', []))
        
        # Check for keywords
        text_lower = cleaned_text.lower()
        
        # Check for product names
        if any(keyword in text_lower for keyword in product_keywords):
            product_names.append(cleaned_text)
        
        # Check for retailer names
        elif any(keyword in text_lower for keyword in retailer_keywords):
            retailer_names.append(cleaned_text)
            
        # Check for brand names
        elif any(keyword in text_lower for keyword in brand_keywords):
            brand_names.append(cleaned_text)
        
        # Check if it's a meaningful text (not just symbols)
        elif re.search(r'[a-zA-Z]{3,}', cleaned_text):
            other_details.append(cleaned_text)
    
    return {
        'product_names': list(set(product_names)),
        'retailer_names': list(set(retailer_names)),
        'brand_names': list(set(brand_names)),
        'prices': list(set(prices)),
        'dates': list(set(dates)),
        'weights': list(set(weights)),
        'volumes': list(set(volumes)),
        'percentages': list(set(percentages)),
        'other_details': [d for d in other_details if len(d) > 3][:10]  # Limit to top 10 meaningful details
    }