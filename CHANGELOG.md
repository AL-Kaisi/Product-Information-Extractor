# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Comprehensive configuration management system
- Multiple export formats (JSON, CSV, Excel, Text)
- Batch processing functionality
- Confidence scoring for OCR results
- Visual feedback with text region detection
- Pattern extraction for prices, dates, weights, volumes
- Enhanced keyword dictionaries for products, retailers, brands
- Docker support with Dockerfile and docker-compose
- Pre-commit hooks for code quality
- GitHub Actions CI/CD workflow
- Comprehensive unit tests
- Type hints throughout the codebase
- Multiple preprocessing modes
- Progress indicators during processing
- LICENSE file (MIT)
- CONTRIBUTING.md guidelines
- .env.example file

### Changed
- Improved OCR accuracy with multiple PSM modes
- Enhanced text filtering with regex patterns
- Updated UI with better user experience
- Modernized requirements.txt with version constraints
- Expanded .gitignore file

### Fixed
- Removed duplicate imports in app.py
- Improved error handling throughout the application
- Fixed text extraction confidence filtering

## [1.0.0] - 2025-01-17

### Added
- Initial release
- Basic OCR functionality with Tesseract
- Streamlit web interface
- Image upload and processing
- Text extraction and categorization
- Basic product and retailer detection