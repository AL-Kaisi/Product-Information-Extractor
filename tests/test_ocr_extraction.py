# tests/test_ocr_extraction.py

import pytest
import numpy as np
from utils.ocr_extraction import extract_patterns, filter_text

class TestOCRExtraction:
    
    def test_extract_patterns(self):
        """Test pattern extraction from text."""
        text = "Product costs $19.99, expires 12/31/2025, weight: 500g"
        patterns = extract_patterns(text)
        
        assert len(patterns['prices']) == 1
        assert patterns['prices'][0] == '$19.99'
        
        assert len(patterns['dates']) == 1
        assert patterns['dates'][0] == '12/31/2025'
        
        assert len(patterns['weights']) == 1
        assert patterns['weights'][0] == '500g'
    
    def test_filter_text_with_keywords(self):
        """Test text filtering with keyword matching."""
        texts = ["Tide Detergent", "Random Text", "Walmart Store"]
        confidences = [80.0, 60.0, 90.0]
        
        result = filter_text(texts, confidences)
        
        assert len(result['product_names']) == 1
        assert "Tide Detergent" in result['product_names']
        
        assert len(result['retailer_names']) == 1
        assert "Walmart Store" in result['retailer_names']
    
    def test_confidence_filtering(self):
        """Test that low confidence text is filtered out."""
        texts = ["Good Text", "Bad Text"]
        confidences = [80.0, 20.0]  # Second text below threshold
        
        result = filter_text(texts, confidences, min_confidence=30.0)
        
        assert "Good Text" in str(result)
        assert "Bad Text" not in str(result)
    
    def test_pattern_extraction_edge_cases(self):
        """Test pattern extraction with edge cases."""
        test_cases = {
            "": {},
            "No patterns here": {},
            "$": {},
            "20%": {'percentages': ['20%']},
            "https://example.com": {'urls': ['https://example.com']}
        }
        
        for text, expected in test_cases.items():
            patterns = extract_patterns(text)
            for key, value in expected.items():
                assert patterns.get(key, []) == value