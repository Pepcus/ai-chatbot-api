"""
Filename: image_processing.py
Author: Deepak Nigam
Date created: 2024-06-05
License: MIT License
Description: This file contains image processing related functions.
"""
from utils.logs import logger
from google.cloud import vision
import io

# Initialize the Vision API client
client = vision.ImageAnnotatorClient()

def read_image(image_path):
    """Reads the image file into memory."""
    with io.open(image_path, 'rb') as image_file:
        return image_file.read()

def perform_label_detection(client, image_content):
    """Performs label detection on the image content."""
    image = vision.Image(content=image_content)
    response = client.label_detection(image=image)
    if response.error.message:
        raise Exception(f'{response.error.message}')
    return response.label_annotations

def perform_text_detection(client, image_content):
    """Performs text detection on the image content."""
    image = vision.Image(content=image_content)
    response = client.text_detection(image=image)
    if response.error.message:
        raise Exception(f'{response.error.message}')
    return response.text_annotations

def extract_text_from_image(image_path):

    # Read the image
    image_content = read_image(image_path)
    
    # Perform label detection
    labels = perform_label_detection(client, image_content)
    logger.info('Labels:')
    for label in labels:
        logger.info(label.description)
    
    # Perform text detection
    texts = perform_text_detection(client, image_content)
    detected_text = ' '.join([text.description for text in texts])
    
    logger.info('\nDetected Text:')
    logger.info(detected_text)
    return detected_text