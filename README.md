# Product Information Extractor

## Overview
Product Information Extractor is a Streamlit-based application that allows users to upload images of product labels and extract relevant product details using OCR (Optical Character Recognition). This tool processes images, detects text regions, and classifies text into product names, retailer names, and other details.

## Features
- Upload product images in `.jpeg`, `.jpg`, or `.png` formats.
- Automatic text detection using OpenCV.
- OCR-based text extraction using Tesseract.
- Categorization of text into product names and retailer names.
- User-friendly Streamlit interface.

## Installation

### Prerequisites
Ensure you have the following installed:
- Python (>=3.7)
- pip

### Clone the Repository
```
git clone https://github.com/yourusername/product-information-extractor.git
cd product-information-extractor
```

### Install Dependencies
```
pip install -r requirements.txt
```

### Install Tesseract OCR
Tesseract is required for text extraction. Install it using:

#### Windows
Download and install [Tesseract OCR](https://github.com/UB-Mannheim/tesseract/wiki)

#### macOS (Homebrew)
```
brew install tesseract
```

#### Linux (Ubuntu/Debian)
```
sudo apt install tesseract-ocr
```

## Running the Application
To launch the Streamlit app, run:
```
streamlit run app.py
```

## Project Structure
```
product-information-extractor
├── app.py                 # Streamlit app main script
├── utils
│   ├── preprocessing.py   # Image preprocessing functions
│   ├── ocr_extraction.py  # OCR extraction and text filtering
├── uploaded_images        # Directory for storing uploaded images
├── requirements.txt       # Required dependencies
└── README.md              # Project documentation
```

## Usage
1. Upload an image by clicking the upload button and selecting an image containing product labels.
2. The app will process the image and extract text.
3. Product names and retailer names will be displayed.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing
Contributions are welcome! If you find any issues or want to improve the project, follow these steps:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature-name`).
3. Commit your changes (`git commit -m 'Added new feature'`).
4. Push to the branch (`git push origin feature-name`).
5. Open a Pull Request.

## Contact
For questions or suggestions, reach out at [your-email@example.com](mailto:your-email@example.com) or open an issue in the repository.

---
Happy coding!

