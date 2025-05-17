# OCR Troubleshooting Guide

## Common OCR Issues and Solutions

### 1. Poor Text Extraction Results

If you're getting garbled text or incorrect extractions:

1. **Try Different Preprocessing Modes**:
   - `text_optimised` - Best for most product labels
   - `combined` - Good for complex images
   - `otsu` - Works well for high-contrast images
   - `adaptive_threshold` - Best for varying lighting

2. **Adjust Settings**:
   - Lower the minimum confidence to see more results
   - Enable denoising for noisy images
   - Adjust resize width (larger for small text, smaller for large text)

3. **Image Quality Tips**:
   - Ensure good lighting (avoid shadows)
   - Keep camera steady (avoid blur)
   - Capture text at a straight angle (avoid skew)
   - Use high resolution images
   - Ensure text is large enough (at least 20 pixels tall)

### 2. No Text Detected

If no text regions are being detected:

1. **Check Image Quality**:
   - Is the text clearly visible?
   - Is there sufficient contrast between text and background?
   - Is the image too dark or too bright?

2. **Try Manual Adjustments**:
   - Upload a cropped image focusing only on the text area
   - Increase the resize width for small text
   - Try the `text_optimised` preprocessing mode
   - Lower the minimum confidence threshold

3. **Image Preparation**:
   - Crop unnecessary parts of the image
   - Remove reflections or glare
   - Ensure text is horizontal (not at an angle)

### 3. Missing Specific Information

If certain fields (prices, dates, etc.) are not being detected:

1. **Pattern Recognition**:
   - Ensure prices include currency symbols ($, £, €)
   - Dates should be in common formats (MM/DD/YYYY, DD-MM-YYYY)
   - Weights should include units (kg, g, lb, oz)

2. **Keyword Issues**:
   - Product names must contain keywords like "cleaner", "soap", etc.
   - Brand names must match known brands
   - Retailer names must match known retailers

3. **Text Formatting**:
   - Ensure text is not broken across multiple lines unexpectedly
   - Check that special characters are clearly visible

### 4. Confidence Score Issues

If confidence scores are too low:

1. **Image Enhancements**:
   - Use the sidebar settings to enable denoising
   - Try different preprocessing modes
   - Ensure proper image resolution

2. **Text Clarity**:
   - Avoid fancy fonts or stylised text
   - Ensure consistent text size
   - Remove background patterns behind text

### 5. Batch Processing Problems

For issues with multiple images:

1. **Consistent Quality**:
   - Ensure all images have similar quality
   - Use the same capture conditions for all images
   - Apply the same preprocessing mode to all

2. **File Size**:
   - Keep individual images under 5MB
   - Use JPEG format for better compression
   - Resize very large images before uploading

## Best Practices for OCR

1. **Image Capture**:
   - Use good lighting (natural light is best)
   - Avoid shadows across text
   - Keep camera parallel to the label
   - Fill the frame with the label
   - Use macro mode for close-ups

2. **Pre-processing**:
   - Start with `text_optimised` mode
   - Enable denoising for older/damaged labels
   - Use appropriate resize width (1920px default)

3. **Post-processing**:
   - Review extracted text for accuracy
   - Export results immediately
   - Use batch processing for multiple similar images

## Quick Fixes

- **Garbled text**: Try different preprocessing modes
- **Missing text**: Lower confidence threshold
- **Wrong orientation**: Image will auto-rotate, but ensure text is roughly horizontal
- **Partial extraction**: Crop image to focus on important areas
- **Poor confidence**: Improve image quality or lighting

## Advanced Tips

1. **Multiple Attempts**:
   - Try the same image with different settings
   - Compare results from different preprocessing modes
   - Combine results from multiple attempts

2. **Image Editing**:
   - Use external tools to enhance contrast
   - Remove backgrounds if possible
   - Straighten skewed images

3. **Testing**:
   - Start with a clear, simple label
   - Gradually work with more complex images
   - Note which settings work best for your use case