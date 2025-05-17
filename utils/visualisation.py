# utils/visualisation.py

import cv2
import numpy as np
from typing import List, Tuple

def visualise_text_regions(
    image: np.ndarray,
    regions: List[Tuple[int, int, int, int]],
    colour: Tuple[int, int, int] = (0, 255, 0),
    thickness: int = 2
) -> np.ndarray:
    """
    Draw bounding boxes around detected text regions.
    """
    # Make a copy to avoid modifying the original
    visualisation = image.copy()
    
    for i, (x, y, w, h) in enumerate(regions):
        # Draw rectangle
        cv2.rectangle(visualisation, (x, y), (x + w, y + h), colour, thickness)
        
        # Add region number
        cv2.putText(
            visualisation,
            f"R{i+1}",
            (x, y - 5),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            colour,
            1
        )
    
    return visualisation

def create_confidence_heatmap(
    image: np.ndarray,
    regions: List[Tuple[int, int, int, int]],
    confidence_scores: List[float]
) -> np.ndarray:
    """
    Create a heatmap visualisation showing confidence scores for each region.
    """
    # Create a greyscale version of the image
    if len(image.shape) == 3:
        grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        heatmap = cv2.cvtColor(grey, cv2.COLOR_GRAY2BGR)
    else:
        heatmap = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    
    # Create an overlay
    overlay = np.zeros_like(heatmap)
    
    for (x, y, w, h), confidence in zip(regions, confidence_scores):
        # Normalise confidence to 0-255 range
        intensity = int(confidence * 2.55)
        
        # Create colour based on confidence (red = low, green = high)
        if confidence < 50:
            colour = (0, 0, intensity)  # Red
        elif confidence < 75:
            colour = (0, intensity, intensity)  # Yellow
        else:
            colour = (0, intensity, 0)  # Green
        
        # Fill the region
        overlay[y:y+h, x:x+w] = colour
    
    # Blend the overlay with the original image
    alpha = 0.3
    heatmap = cv2.addWeighted(heatmap, 1-alpha, overlay, alpha, 0)
    
    return heatmap

def display_extracted_text(
    image: np.ndarray,
    regions: List[Tuple[int, int, int, int]],
    texts: List[str],
    confidence_scores: List[float]
) -> np.ndarray:
    """
    Display extracted text next to each region with confidence scores.
    """
    visualisation = image.copy()
    
    # Add a white panel on the right for text display
    height, width = image.shape[:2]
    text_panel_width = 400
    full_image = np.ones((height, width + text_panel_width, 3), dtype=np.uint8) * 255
    full_image[:, :width] = visualisation
    
    # Draw regions and add text
    for i, ((x, y, w, h), text, confidence) in enumerate(zip(regions, texts, confidence_scores)):
        # Draw rectangle on image
        colour = (0, 255, 0) if confidence > 70 else (0, 255, 255) if confidence > 40 else (0, 0, 255)
        cv2.rectangle(full_image, (x, y), (x + w, y + h), colour, 2)
        cv2.putText(full_image, f"{i+1}", (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, colour, 1)
        
        # Add text to panel
        text_y = 30 + i * 40
        text_x = width + 10
        
        # Truncate text if too long
        display_text = text[:30] + "..." if len(text) > 30 else text
        
        cv2.putText(
            full_image,
            f"{i+1}: {display_text}",
            (text_x, text_y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (0, 0, 0),
            1
        )
        
        cv2.putText(
            full_image,
            f"Conf: {confidence:.1f}%",
            (text_x, text_y + 15),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.4,
            colour,
            1
        )
    
    return full_image

def create_preprocessing_comparison(
    original: np.ndarray,
    preprocessed_images: dict
) -> np.ndarray:
    """
    Create a grid showing different preprocessing results.
    """
    # Resize all images to the same size
    height, width = 300, 400
    
    images = []
    labels = []
    
    # Add original
    resized_original = cv2.resize(original, (width, height))
    images.append(resized_original)
    labels.append("Original")
    
    # Add preprocessed versions
    for method, img in preprocessed_images.items():
        if len(img.shape) == 2:
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        resized = cv2.resize(img, (width, height))
        images.append(resized)
        labels.append(method)
    
    # Create grid
    rows = 2
    cols = (len(images) + 1) // 2
    
    grid = np.zeros((rows * height, cols * width, 3), dtype=np.uint8)
    
    for i, (img, label) in enumerate(zip(images, labels)):
        row = i // cols
        col = i % cols
        
        y1 = row * height
        y2 = (row + 1) * height
        x1 = col * width
        x2 = (col + 1) * width
        
        grid[y1:y2, x1:x2] = img
        
        # Add label
        cv2.putText(
            grid,
            label,
            (x1 + 10, y1 + 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 255),
            2
        )
    
    return grid