"""Setup configuration for Product Information Extractor."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="product-info-extractor",
    version="1.1.0",
    author="Mohamed Al-Kaisi",
    author_email="malkaisi92@gmail.com",
    description="A powerful OCR-based tool for extracting product information from images",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/Product-Information-Extractor",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Licence :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "black>=23.0.0",
            "mypy>=1.6.0",
            "pre-commit>=3.5.0",
            "isort>=5.12.0",
            "flake8>=6.1.0",
            "pytest-cov>=4.1.0",
        ]
    },
    entry_points={
        "console_scripts": [
            "product-extractor=app:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)