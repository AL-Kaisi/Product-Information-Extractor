#!/bin/bash
set -e

echo "Starting Product Information Extractor..."
echo "Current directory: $(pwd)"
echo "Files in directory:"
ls -la
echo "Python version:"
python --version
echo "Streamlit version:"
streamlit --version
echo "Starting Streamlit app..."

exec streamlit run app.py \
    --server.port=8501 \
    --server.address=0.0.0.0 \
    --server.headless=true \
    --browser.serverAddress=localhost \
    --browser.serverPort=8501