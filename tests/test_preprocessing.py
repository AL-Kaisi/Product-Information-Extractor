# tests/test_preprocessing.py

import pytest
import numpy as np
import cv2
from utils.preprocessing import enhance_contrast, deskew_image

class TestPreprocessing:
    
    def test_enhance_contrast_methods(self):
        """Test different contrast enhancement methods."""
        # Create a test image
        test_image = np.ones((100, 100, 3), dtype=np.uint8) * 128
        
        methods = ["clahe", "histogram_equalisation", "gamma_correction"]
        
        for method in methods:
            enhanced = enhance_contrast(test_image, method=method)
            assert enhanced.shape == test_image.shape
            assert enhanced.dtype == test_image.dtype
    
    def test_deskew_image(self):
        """Test image deskewing functionality."""
        # Create a simple test image
        test_image = np.zeros((100, 100), dtype=np.uint8)
        cv2.line(test_image, (10, 10), (90, 90), 255, 2)
        
        deskewed = deskew_image(test_image)
        assert deskewed.shape == test_image.shape
    
    def test_invalid_preprocessing_mode(self):
        """Test handling of invalid preprocessing mode."""
        # This should use the default preprocessing
        from utils.preprocessing import preprocess_image
        test_image_path = "test_image.jpg"
        
        # Create a dummy image file
        dummy_image = np.ones((100, 100, 3), dtype=np.uint8) * 255
        cv2.imwrite(test_image_path, dummy_image)
        
        try:
            processed, original = preprocess_image(
                test_image_path,
                preprocessing_mode="invalid_mode"
            )
            assert processed.shape[:2] == original.shape[:2]
        finally:
            import os
            if os.path.exists(test_image_path):
                os.remove(test_image_path)