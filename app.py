import streamlit as st
import os
import logging
from typing import List, Tuple, Optional
import cv2
from utils.preprocessing import preprocess_image
from utils.ocr_extraction import extract_text_from_image, filter_text
from utils.data_export import export_to_json, export_to_csv
from utils.visualisation import visualise_text_regions

# Configure logging
logging.basicConfig(level=logging.INFO)

# Upload folder
UPLOAD_FOLDER = 'uploaded_images'
EXTRACTED_FOLDER = 'extracted_info'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(EXTRACTED_FOLDER, exist_ok=True)

# Streamlit app with session state
if 'batch_results' not in st.session_state:
    st.session_state.batch_results = []

st.title("Product Information Extractor")
st.write("Upload an image of a product to extract relevant details.")

# Add preprocessing options
with st.sidebar:
    st.header("Settings")
    preprocessing_mode = st.selectbox(
        "Preprocessing Mode",
        ["adaptive_threshold", "otsu", "morphological", "edge_detection", "combined", "text_optimised"],
        index=5  # Default to text_optimised
    )
    
    min_confidence = st.slider("Minimum Confidence", 0, 100, 30, 5)
    resize_width = st.number_input("Resize Width (pixels)", 0, 3000, 1920)
    denoise = st.checkbox("Apply Denoising", True)
    show_visualisation = st.checkbox("Show Text Regions", True)

# Add batch processing option
process_mode = st.radio("Processing Mode", ["Single Image", "Batch Processing"])

if process_mode == "Single Image":
    uploaded_file = st.file_uploader("Upload an Image", type=["jpeg", "jpg", "png", "bmp"])

    if uploaded_file:
        # Show progress bar
        progress_bar = st.progress(0)
        progress_text = st.empty()
        
        try:
            # Save uploaded image
            progress_text.text("Saving image...")
            progress_bar.progress(10)
            
            image_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)
            with open(image_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            st.success("Image uploaded successfully!")

            # Display the uploaded image
            col1, col2 = st.columns(2)
            with col1:
                st.image(image_path, caption="Uploaded Image", use_column_width=True)

            # Preprocess image
            progress_text.text("Preprocessing image...")
            progress_bar.progress(30)
            
            processed_image, original_image = preprocess_image(
                image_path,
                preprocessing_mode=preprocessing_mode,
                resize_width=resize_width if resize_width > 0 else None,
                denoise=denoise
            )

            # Detect text regions (contours)
            progress_text.text("Detecting text regions...")
            progress_bar.progress(50)
            
            contours, _ = cv2.findContours(processed_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            text_regions = [cv2.boundingRect(c) for c in contours if cv2.contourArea(c) > 100]

            if text_regions or preprocessing_mode == "text_optimised":
                if text_regions:
                    logging.info(f"Detected {len(text_regions)} text regions.")
                else:
                    # Use whole image as single region for text_optimised mode
                    h, w = original_image.shape[:2]
                    text_regions = [(0, 0, w, h)]
                
                # Visualise detected regions
                if show_visualisation:
                    with col2:
                        visualisation = visualise_text_regions(original_image, text_regions)
                        st.image(visualisation, caption="Detected Text Regions", use_column_width=True)

                # Extract text
                progress_text.text("Extracting text...")
                progress_bar.progress(70)
                
                extracted_texts, confidence_scores = extract_text_from_image(original_image, text_regions)
                
                # Enhanced filtering
                progress_text.text("Analysing extracted text...")
                progress_bar.progress(90)
                
                product_info = filter_text(extracted_texts, confidence_scores, min_confidence=min_confidence)

                # Display extracted information
                st.subheader("Extracted Product Information")
                
                # Create columns for better display
                info_col1, info_col2 = st.columns(2)
                
                with info_col1:
                    st.write("**Product Names:**")
                    if product_info['product_names']:
                        for name in product_info['product_names']:
                            st.write(f"- {name}")
                    else:
                        st.write("Not Detected")
                    
                    st.write("")
                    st.write("**Brand Names:**")
                    if product_info.get('brand_names'):
                        for brand in product_info['brand_names']:
                            st.write(f"- {brand}")
                    else:
                        st.write("Not Detected")
                    
                    st.write("")
                    st.write("**Prices:**")
                    if product_info['prices']:
                        for price in product_info['prices']:
                            st.write(f"- {price}")
                    else:
                        st.write("Not Detected")
                
                with info_col2:
                    st.write("**Retailer Names:**")
                    if product_info['retailer_names']:
                        for retailer in product_info['retailer_names']:
                            st.write(f"- {retailer}")
                    else:
                        st.write("Not Detected")
                    
                    st.write("")
                    st.write("**Dates:**")
                    if product_info['dates']:
                        for date in product_info['dates']:
                            st.write(f"- {date}")
                    else:
                        st.write("Not Detected")
                    
                    st.write("")
                    st.write("**Weights/Volumes:**")
                    weights = product_info.get('weights', [])
                    volumes = product_info.get('volumes', [])
                    measurements = weights + volumes
                    if measurements:
                        for measure in measurements:
                            st.write(f"- {measure}")
                    else:
                        st.write("Not Detected")
                
                # Other details in expander
                with st.expander("View Other Details"):
                    if product_info['other_details']:
                        for detail in product_info['other_details']:
                            st.write(f"- {detail}")
                    else:
                        st.write("No additional details found")
                
                # Show confidence scores
                if confidence_scores:
                    avg_confidence = sum(confidence_scores) / len(confidence_scores)
                    st.metric("Average Confidence", f"{avg_confidence:.1f}%")
                
                # Export options
                st.subheader("Export Options")
                col1, col2 = st.columns(2)
                
                with col1:
                    if st.button("Export as JSON"):
                        filename = export_to_json(uploaded_file.name, product_info, EXTRACTED_FOLDER)
                        st.success(f"Exported to {filename}")
                        
                with col2:
                    if st.button("Export as CSV"):
                        filename = export_to_csv(uploaded_file.name, product_info, EXTRACTED_FOLDER)
                        st.success(f"Exported to {filename}")
                
                progress_bar.progress(100)
                progress_text.text("Processing complete!")
                
            else:
                st.warning("No text regions detected. Try a different preprocessing mode or clearer image.")
        
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            logging.error(f"Error processing image: {str(e)}")
            
else:  # Batch Processing
    uploaded_files = st.file_uploader(
        "Upload Multiple Images", 
        type=["jpeg", "jpg", "png", "bmp"],
        accept_multiple_files=True
    )
    
    if uploaded_files:
        st.write(f"Processing {len(uploaded_files)} images...")
        
        batch_results = []
        batch_progress = st.progress(0)
        
        for idx, uploaded_file in enumerate(uploaded_files):
            result = {
                "filename": uploaded_file.name,
                "status": "processing"
            }
            
            try:
                # Save uploaded image
                image_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)
                with open(image_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                # Process image
                processed_image, original_image = preprocess_image(
                    image_path,
                    preprocessing_mode=preprocessing_mode,
                    resize_width=resize_width if resize_width > 0 else None,
                    denoise=denoise
                )
                contours, _ = cv2.findContours(processed_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                text_regions = [cv2.boundingRect(c) for c in contours if cv2.contourArea(c) > 100]
                
                if text_regions:
                    extracted_texts, confidence_scores = extract_text_from_image(original_image, text_regions)
                    product_info = filter_text(extracted_texts, confidence_scores, min_confidence=min_confidence)
                    
                    result["status"] = "success"
                    result["product_info"] = product_info
                else:
                    result["status"] = "no_text_detected"
                    
            except Exception as e:
                result["status"] = f"error: {str(e)}"
                logging.error(f"Error processing {uploaded_file.name}: {str(e)}")
            
            batch_results.append(result)
            batch_progress.progress((idx + 1) / len(uploaded_files))
        
        # Display batch results
        st.subheader("Batch Processing Results")
        
        success_count = sum(1 for r in batch_results if r["status"] == "success")
        no_text_count = sum(1 for r in batch_results if r["status"] == "no_text_detected")
        error_count = sum(1 for r in batch_results if r["status"].startswith("error"))
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Successful", success_count)
        col2.metric("No Text", no_text_count)
        col3.metric("Errors", error_count)
        
        # Display detailed results
        with st.expander("View Detailed Results"):
            for result in batch_results:
                st.write(f"**{result['filename']}**")
                if result["status"] == "success":
                    info = result['product_info']
                    st.write(f"- Products: {', '.join(info['product_names']) or 'None'}")
                    st.write(f"- Retailers: {', '.join(info['retailer_names']) or 'None'}")
                    st.write(f"- Prices: {', '.join(info['prices']) or 'None'}")
                else:
                    st.write(f"- Status: {result['status']}")
                st.write("---")
        
        # Export batch results
        if st.button("Export Batch Results"):
            from utils.data_export import export_batch_results
            filename = export_batch_results(batch_results, EXTRACTED_FOLDER)
            st.success(f"Batch results exported to {filename}")