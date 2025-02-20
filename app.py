import streamlit as st
import os
import logging
from utils.preprocessing import preprocess_image
from utils.ocr_extraction import extract_text_from_image, filter_text
import cv2
from utils.preprocessing import preprocess_image

# Configure logging
logging.basicConfig(level=logging.INFO)

# Upload folder
UPLOAD_FOLDER = 'uploaded_images'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Streamlit app
st.title("🧠 Product Information Extractor")
st.write("Upload an image of a product to extract relevant details.")

uploaded_file = st.file_uploader("Upload an Image", type=["jpeg", "jpg", "png"])

if uploaded_file:
    # Save uploaded image
    image_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)
    with open(image_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.success("✅ Image uploaded successfully!")

    # Display the uploaded image
    st.image(image_path, caption="Uploaded Image", use_column_width=True)

    # Preprocess image
    processed_image, original_image = preprocess_image(image_path)

    # Detect text regions (contours)
    contours, _ = cv2.findContours(processed_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    text_regions = [cv2.boundingRect(c) for c in contours if cv2.contourArea(c) > 100]

    if text_regions:
        logging.info(f"Detected {len(text_regions)} text regions.")

        # Extract text
        extracted_texts = extract_text_from_image(original_image, text_regions)
        product_names, retailer_names = filter_text(extracted_texts)

        # Display extracted information
        st.subheader("🔍 Extracted Product Information")
        st.write(f"**Product Names:** {', '.join(product_names) if product_names else 'Not Detected'}")
        st.write(f"**Retailer Names:** {', '.join(retailer_names) if retailer_names else 'Not Detected'}")
        st.write(f"**Other Details:** {', '.join(extracted_texts)}")
    else:
        st.warning("⚠️ No text regions detected. Try a clearer image.")
