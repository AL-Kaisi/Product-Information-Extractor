def preprocess_image(image_path):
    """
    Preprocess the image for better OCR results.
    Returns both processed image and the original image.
    """
    import cv2

    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Could not load image from path: {image_path}")

    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian Blur to reduce noise
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Adaptive thresholding
    binary = cv2.adaptiveThreshold(
        blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
    )

    return binary, image  # Only return two values
