# utils/preprocessing.py

import cv2
import numpy as np
from typing import Tuple, Optional
from scipy import ndimage
import math

def preprocess_image(
    image_path: str,
    preprocessing_mode: str = "adaptive_threshold",
    resize_width: Optional[int] = None,
    denoise: bool = True
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Preprocess the image for better OCR results with multiple preprocessing options.
    Returns both processed image and the original image.
    """
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Could not load image from path: {image_path}")

    # Make a copy of the original
    original_image = image.copy()

    # Auto-rotate image if needed
    rotated_image = auto_rotate_image(image)
    
    # Resize if specified or if image is too large
    if resize_width or rotated_image.shape[1] > 2000:
        resize_width = resize_width or 1920
        aspect_ratio = rotated_image.shape[0] / rotated_image.shape[1]
        resize_height = int(resize_width * aspect_ratio)
        rotated_image = cv2.resize(rotated_image, (resize_width, resize_height), interpolation=cv2.INTER_AREA)

    # Convert to greyscale
    grey = cv2.cvtColor(rotated_image, cv2.COLOR_BGR2GRAY)

    # Denoise if requested
    if denoise:
        grey = cv2.fastNlMeansDenoising(grey)

    # Apply selected preprocessing mode
    if preprocessing_mode == "adaptive_threshold":
        binary = apply_adaptive_threshold(grey)
    
    elif preprocessing_mode == "otsu":
        binary = apply_otsu_threshold(grey)
    
    elif preprocessing_mode == "morphological":
        binary = apply_morphological_operations(grey)
    
    elif preprocessing_mode == "edge_detection":
        binary = apply_edge_detection(grey)
    
    elif preprocessing_mode == "combined":
        binary = apply_combined_preprocessing(grey)
        
    elif preprocessing_mode == "text_optimised":
        binary = apply_text_optimised_preprocessing(grey)
    
    else:
        # Default to simple binary threshold
        _, binary = cv2.threshold(grey, 127, 255, cv2.THRESH_BINARY)

    return binary, original_image

def apply_adaptive_threshold(grey: np.ndarray) -> np.ndarray:
    """Apply adaptive thresholding - good for varying lighting conditions."""
    blurred = cv2.GaussianBlur(grey, (5, 5), 0)
    binary = cv2.adaptiveThreshold(
        blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
    )
    return binary

def apply_otsu_threshold(grey: np.ndarray) -> np.ndarray:
    """Apply OTSU thresholding - automatic threshold selection."""
    blur = cv2.GaussianBlur(grey, (5, 5), 0)
    _, binary = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return binary

def apply_morphological_operations(grey: np.ndarray) -> np.ndarray:
    """Apply morphological operations - good for removing noise and connecting broken text."""
    _, binary = cv2.threshold(grey, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    kernel = np.ones((2, 2), np.uint8)
    binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
    binary = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)
    return binary

def apply_edge_detection(grey: np.ndarray) -> np.ndarray:
    """Apply edge detection - good for extracting text boundaries."""
    edges = cv2.Canny(grey, 100, 200)
    binary = 255 - edges
    return binary

def apply_combined_preprocessing(grey: np.ndarray) -> np.ndarray:
    """Apply combined approach - uses multiple techniques."""
    # Apply CLAHE for contrast enhancement
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    enhanced = clahe.apply(grey)
    
    # Apply bilateral filter to reduce noise while keeping edges sharp
    filtered = cv2.bilateralFilter(enhanced, 9, 75, 75)
    
    # Apply adaptive thresholding
    binary = cv2.adaptiveThreshold(
        filtered, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
    )
    
    # Clean up with morphological operations
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
    binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
    
    return binary

def apply_text_optimised_preprocessing(grey: np.ndarray) -> np.ndarray:
    """Apply preprocessing optimised for text extraction."""
    # Increase image size if too small
    height, width = grey.shape
    if height < 300 or width < 300:
        scale_factor = max(300/height, 300/width)
        new_width = int(width * scale_factor)
        new_height = int(height * scale_factor)
        grey = cv2.resize(grey, (new_width, new_height), interpolation=cv2.INTER_CUBIC)
    
    # Apply sharpening
    kernel = np.array([[0, -1, 0],
                      [-1, 5, -1],
                      [0, -1, 0]])
    sharpened = cv2.filter2D(grey, -1, kernel)
    
    # Apply CLAHE for better contrast
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
    enhanced = clahe.apply(sharpened)
    
    # Binary threshold with OTSU
    _, binary = cv2.threshold(enhanced, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    # Remove noise
    kernel = np.ones((1, 1), np.uint8)
    binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
    
    return binary

def auto_rotate_image(image: np.ndarray) -> np.ndarray:
    """Automatically rotate image to correct orientation using text detection."""
    grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Detect edges
    edges = cv2.Canny(grey, 50, 150, apertureSize=3)
    
    # Detect lines
    lines = cv2.HoughLines(edges, 1, np.pi/180, 100)
    
    if lines is not None:
        angles = []
        for rho, theta in lines[:, 0]:
            angle = np.degrees(theta) - 90
            if -45 < angle < 45:  # Only consider small rotations
                angles.append(angle)
        
        if angles:
            median_angle = np.median(angles)
            if abs(median_angle) > 0.5:  # Only rotate if angle is significant
                return rotate_image(image, median_angle)
    
    return image

def rotate_image(image: np.ndarray, angle: float) -> np.ndarray:
    """Rotate image by specified angle."""
    (h, w) = image.shape[:2]
    centre = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(centre, angle, 1.0)
    
    # Calculate new image bounds
    cos = np.abs(M[0, 0])
    sin = np.abs(M[0, 1])
    new_w = int((h * sin) + (w * cos))
    new_h = int((h * cos) + (w * sin))
    
    # Adjust rotation matrix
    M[0, 2] += (new_w / 2) - centre[0]
    M[1, 2] += (new_h / 2) - centre[1]
    
    return cv2.warpAffine(image, M, (new_w, new_h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

def deskew_image(image: np.ndarray) -> np.ndarray:
    """
    Deskew the image to correct for any rotation.
    """
    # Convert to greyscale if not already
    if len(image.shape) == 3:
        grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        grey = image.copy()
    
    # Apply threshold to get binary image
    _, binary = cv2.threshold(grey, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    
    # Find all non-zero pixels
    coords = np.column_stack(np.where(binary > 0))
    
    if len(coords) == 0:
        return image
    
    # Calculate the skew angle
    angle = cv2.minAreaRect(coords)[-1]
    
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle
    
    # Skip small angles
    if abs(angle) < 0.5:
        return image
    
    # Rotate the image to deskew
    return rotate_image(image, angle)

def remove_shadows(image: np.ndarray) -> np.ndarray:
    """
    Remove shadows from the image.
    """
    # Convert to LAB colour space
    lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    
    # Apply CLAHE to L channel
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
    l = clahe.apply(l)
    
    # Merge channels
    enhanced = cv2.merge([l, a, b])
    
    # Convert back to BGR
    enhanced = cv2.cvtColor(enhanced, cv2.COLOR_LAB2BGR)
    
    return enhanced

def enhance_contrast(image: np.ndarray, method: str = "clahe") -> np.ndarray:
    """
    Enhance image contrast using different methods.
    """
    if method == "clahe":
        # Convert to LAB colour space
        lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        
        # Apply CLAHE to L channel
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
        l = clahe.apply(l)
        
        # Merge channels
        enhanced = cv2.merge([l, a, b])
        enhanced = cv2.cvtColor(enhanced, cv2.COLOR_LAB2BGR)
    
    elif method == "histogram_equalisation":
        # Convert to YCrCb
        ycrcb = cv2.cvtColor(image, cv2.COLOR_BGR2YCrCb)
        y, cr, cb = cv2.split(ycrcb)
        
        # Apply histogram equalisation to Y channel
        y = cv2.equalizeHist(y)
        
        # Merge channels
        enhanced = cv2.merge([y, cr, cb])
        enhanced = cv2.cvtColor(enhanced, cv2.COLOR_YCrCb2BGR)
    
    elif method == "gamma_correction":
        # Apply gamma correction
        gamma = 1.5
        invGamma = 1.0 / gamma
        table = np.array([((i / 255.0) ** invGamma) * 255 for i in np.arange(0, 256)]).astype("uint8")
        enhanced = cv2.LUT(image, table)
    
    else:
        enhanced = image
    
    return enhanced