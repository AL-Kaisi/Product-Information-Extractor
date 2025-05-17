FROM python:3.9-slim

# Install system dependencies for OpenCV and Tesseract
RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    libgl1-mesa-glx \
    libgtk-3-0 \
    tesseract-ocr \
    tesseract-ocr-eng \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application files
COPY app.py .
COPY config.py .
COPY utils/ ./utils/
COPY .streamlit/ ./.streamlit/
COPY entrypoint.sh .

# Create necessary directories
RUN mkdir -p uploaded_images extracted_info

# Make entrypoint executable
RUN chmod +x entrypoint.sh

# Set Python path
ENV PYTHONPATH=/app

# Expose Streamlit port
EXPOSE 8501

# Run the application
ENTRYPOINT ["./entrypoint.sh"]