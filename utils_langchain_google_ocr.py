from google.cloud import vision
import os
from openai import OpenAI
from utils_langchain_sql import get_sql_query_agent

GPT_MODEL = "gpt-3.5-turbo"
client = OpenAI()

# Set up Google Cloud Vision API credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'gcp_creds.json'

# Function to extract text from an image using Google Cloud Vision API
def read_document_through_google_ocr(file_location):
    client = vision.ImageAnnotatorClient()
    with open(file_location, 'rb') as file:
         content = file.read()
    image = vision.Image(content=content)
    response = client.text_detection(image=image)
    texts = response.text_annotations
    extracted_text = texts[0].description if texts else ''
    return extracted_text

def process_document_through_google_ocr(db, llm, query, file_location):
    # Extract text from the image
    extracted_text = read_document_through_google_ocr(file_location)
    query = f'''Generate and execute the SQL statement for Postgress Database based on the following information, {query}, {extracted_text}'''
    return  get_sql_query_agent(db, llm, query)