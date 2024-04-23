import os 
import sys
import cv2
from PIL import Image
import base64
from io import BytesIO

from src.logger import logger
from src.exception import CustomException

def find_largest_contour(blurred_image):
    """Find the largest contour in the image

    Args:
        blurred_image (_type_): _description_

    Returns:
        tuple: x, y, w, h (the coordinates of the bounding box of the largest contour)
    """
    try:
        # Find contours
        contours, _ = cv2.findContours(blurred_image.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Find the largest contour
        largest_contour = max(contours, key=cv2.contourArea)

        # Get the bounding box of the largest contour
        x, y, w, h = cv2.boundingRect(largest_contour)

        return x, y, w, h
    
    except Exception as e:
        error_message = CustomException(e, sys)
        logger.error(error_message)

        return None


def preprocess_image(image):
    """Preprocess the raw image. Apply adaptive thresholding, noise removal, and extract the nutritional information label
    using longest contour.

    Args:
        image

    Returns:
        pil image: the processed image
    """
    try:
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Apply adaptive thresholding
        adaptive_thresholded_image = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

        # Noise Removal (Gaussian Blur)
        blurred_image = cv2.GaussianBlur(adaptive_thresholded_image, (5, 5), 0)

        # Find the largest contour
        x, y, w, h = find_largest_contour(blurred_image)

        # Extract the nutritional information label
        cropped_image = blurred_image[y:y+h, x:x+w]

        # Resize the image
        cropped_image = cv2.resize(cropped_image, (256, 256), interpolation=cv2.INTER_AREA)

        # Convert the processed image to PIL Image
        pil_image = Image.fromarray(cropped_image)

        return pil_image
    
    except Exception as e:
        error_message = CustomException(e, sys)
        logger.error(error_message)

        return None
    
def convert_to_base64(image_file_path):
    """
    Convert PIL images to Base64 encoded strings

    :param pil_image: PIL image
    :return: Re-sized Base64 string
    """

    pil_image = Image.open(image_file_path)

    buffered = BytesIO()
    pil_image.save(buffered, format="png")  # You can change the format if needed
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return img_str


def convert_to_html(img_base64):
    """
    Disply base64 encoded string as image

    :param img_base64:  Base64 string
    """
    # Create an HTML img tag with the base64 string as the source
    image_html = f'<img src="data:image/jpeg;base64,{img_base64}" style="max-width: 100%;"/>'
    return image_html