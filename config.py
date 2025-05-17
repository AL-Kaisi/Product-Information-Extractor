# config.py

import os
from typing import Dict, Any

class Config:
    """Configuration management for the Product Information Extractor."""
    
    # Directory configurations
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploaded_images')
    EXTRACTED_FOLDER = os.path.join(BASE_DIR, 'extracted_info')
    
    # OCR configurations
    OCR_CONFIG = {
        'min_confidence': 30.0,
        'psm_modes': [6, 8, 11, 3],
        'padding': 5,
        'language': 'eng'
    }
    
    # Preprocessing configurations
    PREPROCESSING_CONFIG = {
        'default_mode': 'adaptive_threshold',
        'resize_width': 1920,  # Resize images wider than this
        'denoise': True,
        'deskew': False,
        'remove_shadows': False
    }
    
    # Text extraction patterns
    EXTRACTION_PATTERNS = {
        'prices': r'\$?[\d,]+\.?\d*',
        'dates': r'\d{1,2}[-/]\d{1,2}[-/]\d{2,4}|\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{2,4}',
        'percentages': r'\d+\.?\d*\s*%',
        'weights': r'\d+\.?\d*\s*(?:kg|g|mg|lb|oz|lbs|ounces?)',
        'volumes': r'\d+\.?\d*\s*(?:ml|l|L|mL|gal|gallons?)',
        'product_codes': r'[A-Z]{2,}\d{3,}|\d{3,}[A-Z]{2,}',
        'barcodes': r'\d{8,13}',
        'urls': r'https?://\S+|www\.\S+',
        'emails': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    }
    
    # Keyword configurations
    KEYWORDS = {
        'product_keywords': {
            "cleaner", "detergent", "disinfectant", "soda", "borax", "dishwasher",
            "soap", "shampoo", "conditioner", "toothpaste", "mouthwash", "deodorant",
            "lotion", "cream", "gel", "spray", "powder", "liquid", "tablets",
            "bleach", "softener", "freshener", "sanitizer", "wash", "rinse",
            "wipes", "towels", "tissue", "paper", "napkins", "rolls"
        },
        'retailer_keywords': {
            "atlas", "rayhong", "finish", "wrld", "walker", "walmart", "target",
            "costco", "amazon", "safeway", "kroger", "publix", "albertsons",
            "walgreens", "cvs", "rite aid", "whole foods", "trader joe's",
            "meijer", "wegmans", "aldi", "lidl", "dollar general", "family dollar"
        },
        'brand_keywords': {
            "tide", "gain", "downy", "cascade", "dawn", "febreze", "oxi clean",
            "arm & hammer", "lysol", "clorox", "mr. clean", "pine-sol", "ajax",
            "comet", "seventh generation", "method", "mrs. meyer's", "all",
            "persil", "woolite", "shout", "resolve", "pledge", "windex",
            "charmin", "bounty", "scott", "kleenex", "cottonelle", "pampers"
        }
    }
    
    # Export configurations
    EXPORT_CONFIG = {
        'formats': ['json', 'csv', 'txt', 'excel'],
        'default_format': 'json',
        'timestamp_format': '%Y%m%d_%H%M%S'
    }
    
    # UI configurations
    UI_CONFIG = {
        'max_file_size_mb': 10,
        'allowed_extensions': ['jpeg', 'jpg', 'png', 'bmp', 'tiff'],
        'show_confidence_scores': True,
        'show_visualisation': True,
        'batch_processing_limit': 50
    }
    
    @classmethod
    def get_config(cls) -> Dict[str, Any]:
        """Get all configuration as a dictionary."""
        return {
            'directories': {
                'base_dir': cls.BASE_DIR,
                'upload_folder': cls.UPLOAD_FOLDER,
                'extracted_folder': cls.EXTRACTED_FOLDER
            },
            'ocr': cls.OCR_CONFIG,
            'preprocessing': cls.PREPROCESSING_CONFIG,
            'patterns': cls.EXTRACTION_PATTERNS,
            'keywords': cls.KEYWORDS,
            'export': cls.EXPORT_CONFIG,
            'ui': cls.UI_CONFIG
        }
    
    @classmethod
    def ensure_directories(cls):
        """Ensure all required directories exist."""
        os.makedirs(cls.UPLOAD_FOLDER, exist_ok=True)
        os.makedirs(cls.EXTRACTED_FOLDER, exist_ok=True)

# Environment-based configuration
class DevelopmentConfig(Config):
    """Development environment configuration."""
    DEBUG = True
    LOG_LEVEL = 'DEBUG'

class ProductionConfig(Config):
    """Production environment configuration."""
    DEBUG = False
    LOG_LEVEL = 'INFO'

# Configuration factory
def get_config(env: str = 'development') -> Config:
    """Get configuration based on environment."""
    configs = {
        'development': DevelopmentConfig,
        'production': ProductionConfig
    }
    return configs.get(env, DevelopmentConfig)

# Initialize configuration
current_config = get_config(os.getenv('ENVIRONMENT', 'development'))