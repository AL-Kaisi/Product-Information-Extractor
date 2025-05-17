# Product Information Extractor

[![CI](https://github.com/yourusername/Product-Information-Extractor/workflows/CI/badge.svg)](https://github.com/yourusername/Product-Information-Extractor/actions)
[![Licence: MIT](https://img.shields.io/badge/Licence-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## How It Works

```mermaid
graph LR
    A[Product Label Image] --> B[Upload to App]
    B --> C[Image Preprocessing]
    C --> D[Text Detection]
    D --> E[OCR Extraction]
    E --> F[Pattern Recognition]
    F --> G[Categorisation]
    G --> H[Results Display]
    H --> I[Export Data]

    style A fill:#f9f,stroke:#333,stroke-width:2px
    style E fill:#bbf,stroke:#333,stroke-width:2px
    style H fill:#bfb,stroke:#333,stroke-width:2px
```

## Quick Start

```bash
# Clone the repository
git clone https://github.com/yourusername/Product-Information-Extractor.git
cd Product-Information-Extractor

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Verify installation
python -c "import streamlit; import cv2; import pytesseract; print('All packages installed successfully!')"

# Run the app
streamlit run app.py
```

## Overview
Product Information Extractor is a powerful Streamlit-based application that uses advanced OCR (Optical Character Recognition) technology to extract product details from images. The tool processes images, detects text regions, and intelligently categorises text into product names, retailer names, prices, dates, and other relevant information.

## System Architecture

```mermaid
graph TB
    A[User Interface<br/>Streamlit App] --> B[Image Upload]
    B --> C[Preprocessing Module]
    C --> D[Text Detection<br/>OpenCV]
    D --> E[OCR Engine<br/>Tesseract]
    E --> F[Text Extraction]
    F --> G[Pattern Recognition<br/>& Filtering]
    G --> H[Data Export]

    C --> C1[Adaptive Threshold]
    C --> C2[OTSU]
    C --> C3[Morphological]
    C --> C4[Edge Detection]
    C --> C5[Combined]
    C --> C6[Text Optimised]

    H --> H1[JSON]
    H --> H2[CSV]
    H --> H3[Excel]
    H --> H4[Text]

    style A fill:#f9f,stroke:#333,stroke-width:4px
    style E fill:#bbf,stroke:#333,stroke-width:4px
    style G fill:#bfb,stroke:#333,stroke-width:4px
```

## Processing Workflow

```mermaid
sequenceDiagram
    participant User
    participant UI as Streamlit UI
    participant Pre as Preprocessing
    participant OCR as OCR Engine
    participant Filter as Text Filter
    participant Export as Data Export

    User->>UI: Upload Image
    UI->>Pre: Send Image
    Pre->>Pre: Apply Enhancement
    Pre->>Pre: Detect Text Regions
    Pre->>OCR: Process Regions

    loop For Each Region
        OCR->>OCR: Extract Text
        OCR->>OCR: Calculate Confidence
    end

    OCR->>Filter: Send Extracted Text
    Filter->>Filter: Apply Patterns
    Filter->>Filter: Categorise Text
    Filter->>UI: Return Results

    UI->>User: Display Results
    User->>UI: Request Export
    UI->>Export: Export Data
    Export->>User: Download File
```

## Features
- **Image Upload**: Support for `.jpeg`, `.jpg`, `.png`, and `.bmp` formats
- **Advanced Text Detection**: Using OpenCV for accurate text region detection
- **Smart OCR**: Enhanced Tesseract OCR with confidence scoring
- **Pattern Recognition**: Automatic extraction of prices, dates, weights, volumes, and more
- **Intelligent Categorisation**: Identifies product names, retailers, and brands
- **Confidence Scoring**: Shows confidence levels for extracted text
- **Visual Feedback**: Displays detected text regions on images
- **Multiple Preprocessing Modes**: Various image enhancement techniques
- **Batch Processing**: Process multiple images at once
- **Multiple Export Formats**: JSON, CSV, Excel, and Text
- **Docker Support**: Easy deployment with Docker and docker-compose
- **Comprehensive Tests**: Unit tests for core functionality
- **CI/CD**: GitHub Actions workflow for continuous integration

## Data Flow

```mermaid
flowchart LR
    A[Product Image] --> B{Preprocessing<br/>Mode}
    B -->|Adaptive| C[Adaptive Threshold]
    B -->|OTSU| D[OTSU Threshold]
    B -->|Morphological| E[Morphological Ops]
    B -->|Edge Detection| F[Edge Detection]
    B -->|Combined| G[Combined Methods]
    B -->|Text Optimised| H[Text Optimised]

    C --> I[Contour Detection]
    D --> I
    E --> I
    F --> I
    G --> I
    H --> I

    I --> J[Text Regions]
    J --> K[OCR Processing]
    K --> L{Confidence<br/>Check}

    L -->|High| M[Pattern Matching]
    L -->|Low| N[Discard]

    M --> O[Text Categories]
    O --> P[Product Names]
    O --> Q[Brand Names]
    O --> R[Retailers]
    O --> S[Prices]
    O --> T[Dates]
    O --> U[Weights/Volumes]

    P --> V[Export Formats]
    Q --> V
    R --> V
    S --> V
    T --> V
    U --> V
```

## Component Interaction

```mermaid
graph TD
    subgraph Frontend
        A[Streamlit UI]
        B[Settings Sidebar]
        C[File Uploader]
        D[Results Display]
        E[Export Buttons]
    end

    subgraph Backend
        F[app.py]
        G[config.py]

        subgraph Utils
            H[preprocessing.py]
            I[ocr_extraction.py]
            J[visualisation.py]
            K[data_export.py]
        end
    end

    subgraph External
        L[OpenCV]
        M[Tesseract OCR]
        N[File System]
    end

    A --> F
    B --> F
    C --> F
    F --> H
    F --> I
    F --> J
    F --> K
    H --> L
    I --> M
    K --> N
    G --> I

    style A fill:#f9f,stroke:#333,stroke-width:2px
    style F fill:#bbf,stroke:#333,stroke-width:2px
    style M fill:#bfb,stroke:#333,stroke-width:2px
```

## Installation

### Prerequisites
- Python (>=3.8)
- pip
- Tesseract OCR

### Clone the Repository
```bash
git clone https://github.com/yourusername/Product-Information-Extractor.git
cd Product-Information-Extractor
```

### Set Up Python Environment

#### Option 1: Using venv (Recommended)
```bash
# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

#### Option 2: Using conda
```bash
# Create a conda environment
conda create -n product-extractor python=3.9

# Activate the environment
conda activate product-extractor

# Install dependencies
pip install -r requirements.txt
```

#### Option 3: Using system Python
```bash
# Install dependencies directly (not recommended for production)
pip3 install -r requirements.txt
```

### Install Tesseract OCR

#### Windows
Download and install [Tesseract OCR](https://github.com/UB-Mannheim/tesseract/wiki)

#### macOS (Homebrew)
```bash
brew install tesseract
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt-get update
sudo apt-get install tesseract-ocr tesseract-ocr-eng
```

## Usage

### Running the Application

1. **Ensure your virtual environment is activated** (if using one):
   ```bash
   # On macOS/Linux:
   source venv/bin/activate
   # On Windows:
   venv\Scripts\activate
   ```

2. **Run the Streamlit app**:
   ```bash
   streamlit run app.py
   ```

   Or if you have issues with the streamlit command:
   ```bash
   python -m streamlit run app.py
   ```

3. **Access the application**:
   - The app will automatically open in your default web browser
   - If not, navigate to: `http://localhost:8501`
   - You should see the Product Information Extractor interface

4. **Stop the application**:
   - Press `Ctrl+C` in the terminal
   - Deactivate the virtual environment when done:
     ```bash
     deactivate
     ```

### Docker Deployment

1. **Build and run with docker-compose**:
   ```bash
   docker-compose up --build
   ```

2. **Or build manually**:
   ```bash
   docker build -t product-info-extractor .
   docker run -p 8501:8501 -v $(pwd)/uploaded_images:/app/uploaded_images -v $(pwd)/extracted_info:/app/extracted_info product-info-extractor
   ```

3. **Access the application**:
   - Open your browser to: `http://localhost:8501`
   - The app should load automatically

4. **Check logs if you encounter issues**:
   ```bash
   docker-compose logs -f
   ```

5. **Test the container**:
   ```bash
   docker-compose exec app python test_imports.py
   ```

### Using the Application
1. Choose between **Single Image** or **Batch Processing** mode
2. Upload image(s) containing product labels
3. Select preprocessing options if needed
4. View extracted information with confidence scores
5. Export results in your preferred format

## Preprocessing Mode Selection Guide

```mermaid
graph TD
    A[Start] --> B{Is the image<br/>quality good?}
    B -->|Yes| C{Is lighting<br/>uniform?}
    B -->|No| D[Use Text Optimised]

    C -->|Yes| E{Is contrast<br/>high?}
    C -->|No| F[Use Adaptive Threshold]

    E -->|Yes| G[Use OTSU]
    E -->|No| H{Complex<br/>background?}

    H -->|Yes| I[Use Combined]
    H -->|No| J[Use Morphological]

    D --> K[Result]
    F --> K
    G --> K
    I --> K
    J --> K

    style A fill:#f9f,stroke:#333,stroke-width:2px
    style K fill:#bfb,stroke:#333,stroke-width:2px
    style D fill:#bbf,stroke:#333,stroke-width:2px
```

## Project Structure
```
product-information-extractor/
├── app.py                      # Streamlit application main file
├── config.py                   # Configuration management
├── utils/
│   ├── preprocessing.py        # Image preprocessing functions
│   ├── ocr_extraction.py       # OCR and text extraction logic
│   ├── data_export.py          # Export functionality
│   └── visualisation.py        # Visualisation utilities
├── tests/
│   ├── test_preprocessing.py   # Preprocessing tests
│   └── test_ocr_extraction.py  # OCR extraction tests
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Docker configuration
├── docker-compose.yml          # Docker Compose configuration
├── .pre-commit-config.yaml     # Pre-commit hooks configuration
├── .github/workflows/ci.yml    # GitHub Actions CI workflow
└── README.md                   # Project documentation
```

## Configuration

The application uses a comprehensive configuration system (`config.py`) that includes:

- **OCR Settings**: Confidence thresholds, PSM modes, language settings
- **Preprocessing Options**: Image enhancement techniques, resize settings
- **Pattern Extraction**: Regular expressions for prices, dates, weights, etc.
- **Keyword Dictionaries**: Extensive lists of products, retailers, and brands
- **Export Options**: Available formats and timestamp settings
- **UI Settings**: File size limits, allowed extensions, batch processing limits

## Development

### Setting up Development Environment
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install pre-commit hooks
pre-commit install
```

### Running Tests
```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ -v --cov=utils --cov-report=html
```

### Code Quality Tools
```bash
# Format code with Black
black .

# Sort imports with isort
isort .

# Run linting
flake8 . --max-line-length=88 --extend-ignore=E203,W503

# Type checking
mypy . --ignore-missing-imports
```

## Key Functions

```mermaid
classDiagram
    class PreprocessingModule {
        +preprocess_image(image_path, mode, resize_width, denoise)
        +apply_adaptive_threshold(grey)
        +apply_otsu_threshold(grey)
        +apply_morphological_operations(grey)
        +apply_edge_detection(grey)
        +apply_combined_preprocessing(grey)
        +apply_text_optimised_preprocessing(grey)
        +auto_rotate_image(image)
        +deskew_image(image)
        +enhance_contrast(image, method)
    }

    class OCRModule {
        +extract_text_from_image(image, regions)
        +extract_text_with_confidence(image, config)
        +enhance_image_for_ocr(image)
        +preprocess_for_text_detection(image)
        +extract_patterns(text)
        +filter_text(texts, scores, min_confidence)
    }

    class VisualisationModule {
        +visualise_text_regions(image, regions, colour, thickness)
        +create_confidence_heatmap(image, regions, scores)
        +display_extracted_text(image, regions, texts, scores)
        +create_preprocessing_comparison(original, processed)
    }

    class DataExportModule {
        +export_to_json(filename, data, output_dir)
        +export_to_csv(filename, data, output_dir)
        +export_to_excel(filename, data, output_dir)
        +export_to_text(filename, data, output_dir)
        +export_batch_results(results, output_dir)
    }

    class Config {
        +OCR_CONFIG
        +PREPROCESSING_CONFIG
        +EXTRACTION_PATTERNS
        +KEYWORDS
        +EXPORT_CONFIG
        +UI_CONFIG
        +get_config()
        +ensure_directories()
    }

    PreprocessingModule --> OCRModule : processed images
    OCRModule --> VisualisationModule : text regions
    OCRModule --> DataExportModule : extracted data
    Config --> OCRModule : configuration
    Config --> PreprocessingModule : settings
```

## Deployment Architecture

```mermaid
graph TB
    subgraph "Docker Container"
        A[Python 3.9 Runtime]
        B[Streamlit Server]
        C[Application Code]
        D[Tesseract OCR]
        E[OpenCV Libraries]
    end

    subgraph "Volumes"
        F[uploaded_images/]
        G[extracted_info/]
    end

    subgraph "User Access"
        H[Web Browser]
    end

    subgraph "Configuration"
        I[.streamlit/config.toml]
        J[config.py]
        K[.env]
    end

    H -->|HTTP:8501| B
    B --> C
    C --> D
    C --> E
    C --> F
    C --> G
    C --> I
    C --> J
    C --> K

    style A fill:#f9f,stroke:#333,stroke-width:2px
    style B fill:#bbf,stroke:#333,stroke-width:2px
    style H fill:#bfb,stroke:#333,stroke-width:2px
```

## API Reference

### Main Functions

#### `preprocess_image(image_path, preprocessing_mode='adaptive_threshold')`
Preprocesses images for better OCR results. Supports multiple enhancement modes.

#### `extract_text_from_image(image, regions)`
Extracts text from detected regions with confidence scoring.

#### `filter_text(texts, confidences, min_confidence=30.0)`
Filters and categorises extracted text based on keywords and patterns.

#### `export_to_json(filename, data, output_dir)`
Exports extracted data to JSON format with timestamps.

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests and ensure code quality
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

### Development Guidelines
- Follow PEP 8 and use Black for formatting
- Add type hints to all functions
- Write tests for new features
- Update documentation as needed
- Ensure all tests pass before submitting PR

## Licence

This project is licensed under the MIT Licence - see the [LICENCE](LICENCE) file for details.

## Acknowledgements

- OpenCV community for excellent image processing tools
- Tesseract OCR for the powerful text recognition engine
- Streamlit for the intuitive web framework
- All contributors who help improve this project

## Troubleshooting

### Common Issues

1. **ModuleNotFoundError: No module named 'streamlit'**
   ```bash
   # Ensure you're in the virtual environment
   # Then reinstall dependencies
   pip install -r requirements.txt
   ```

2. **Tesseract not found error**
   ```bash
   # macOS
   brew install tesseract

   # Ubuntu/Debian
   sudo apt-get install tesseract-ocr

   # Windows
   # Download installer from: https://github.com/UB-Mannheim/tesseract/wiki
   ```

3. **ImportError: libGL.so.1: cannot open shared object file**
   ```bash
   # Linux systems
   sudo apt-get update
   sudo apt-get install libgl1-mesa-glx
   ```

4. **Port 8501 already in use**
   ```bash
   # Kill the process using the port
   lsof -ti:8501 | xargs kill -9

   # Or run on a different port
   streamlit run app.py --server.port=8502
   ```

5. **Python version issues**
   ```bash
   # Check your Python version
   python --version

   # If needed, use specific Python version
   python3.9 -m venv venv
   ```

6. **Docker: 404 Not Found error**
   ```bash
   # Check if container is running
   docker ps

   # Check container logs
   docker-compose logs -f

   # Rebuild the container
   docker-compose down
   docker-compose up --build

   # Test imports inside container
   docker-compose exec app python test_imports.py
   ```

7. **Docker: Permission denied errors**
   ```bash
   # Fix permissions on local directories
   sudo chown -R $USER:$USER uploaded_images extracted_info
   chmod 755 uploaded_images extracted_info
   ```

8. **Docker: Container won't start**
   ```bash
   # Remove old containers and volumes
   docker-compose down -v
   docker system prune -f

   # Rebuild from scratch
   docker-compose build --no-cache
   docker-compose up
   ```

### Getting Help

- Check the [Issues](https://github.com/yourusername/Product-Information-Extractor/issues) page
- Read the error messages carefully - they often contain the solution
- Ensure all prerequisites are properly installed
- Try running with Docker if you have persistent environment issues

## Contact

For questions or suggestions, reach out at [malkaisi92@gmail.com](mailto:malkaisi92@gmail.com) or open an issue in the repository.

---
Made with care by Mohamed Al-Kaisi