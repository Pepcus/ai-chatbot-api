"""
Filename: general.py
Author: Deepak Nigam
Date created: 2024-04-28
License: MIT License
Description: This file contains generic functions.
"""

from langchain_community.document_loaders.pdf import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from config.config import local_download_path
from utils.logs import logger
import os
from utils.image_processing import extract_text_from_image
import fitz
import mimetypes
import pandas as pd
from docx import Document
import csv

def delete_file_from_local(file_name):
    try:
        local_file_path = local_download_path + file_name
        os.remove(local_file_path)
        logger.info(f"Local file {local_file_path} deleted successfully")
    except OSError as e:
        logger.error(f"Error deleting local file: {e}")

## Load the document
def load_doc(directory):
    try:
        # Attempt to load the document
        loader = PyPDFLoader(directory)
        documents = loader.load()
        return documents
    except Exception as e:
        logger.error(f"An error occurred while loading the document: {e}")
        return None

## Divide the docs into chunks
### https://api.python.langchain.com/en/latest/text_splitter/langchain.text_splitter.RecursiveCharacterTextSplitter.html#
def chunk_data(docs, chunk_size=1500, chunk_overlap=200):
    try:
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap, length_function=len)
        doc = text_splitter.split_documents(docs)
        return doc
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        return None
    
def get_file_type(filename):
    mime_type, _ = mimetypes.guess_type(filename)
    if (mime_type == None):
        parts = filename.split('.')
        extension = parts[-1]
        return extension
    return mime_type

def extract_text_from_pdf(pdf_path):
    text = ""
    with fitz.open(pdf_path) as pdf:
        for page in pdf:
            text += page.get_text()
    return text

def extract_text_from_xlsx(file_path):
    # Load the Excel file into a pandas DataFrame
    data = pd.read_excel(file_path)
    
    # Export the DataFrame to a CSV file
    csv_file_path = file_path.replace('.xlsx', '_output.csv')
    data.to_csv(csv_file_path, index=False)
    
    # Read the CSV file as text
    with open(csv_file_path, 'r') as file:
        text_data = file.read()
    
    # Return the text data
    return text_data

def extract_text_from_docx(docx_file):
    doc = Document(docx_file)
    
    # Initialize an empty list to store the table data
    table_data = []

    # Iterate over all tables in the document
    for table in doc.tables:
        # Iterate over all rows in the table
        for row in table.rows:
            # Initialize an empty list to store row data
            row_data = []
            # Iterate over all cells in the row
            for cell in row.cells:
                # Append the text of each cell to row_data list
                row_data.append(cell.text.strip())
            # Append the row_data list to table_data list
            table_data.append(row_data)

    text = ""

    # Iterate over each row in the table data
    for row in table_data:
        # Join the row elements with a tab separator and append it to the text
        text += '\t'.join(row) + '\n'

    return text

def extract_text_from_csv(file_path):
    with open(file_path, 'r', newline='') as file:
        reader = csv.reader(file)
        text = ""
        for row in reader:
            text += ','.join(row) + '\n'
    return text

def extract_text_from_file(file_path):
    with open(file_path, 'r') as file:
        text = file.read()
    return text
     
def extract_text_based_on_file_type(file_type, file_path):
    extraction_functions = {
        'application/pdf': extract_text_from_pdf,
        'xlsx': extract_text_from_xlsx,
        'docx': extract_text_from_docx,
        'text/csv': extract_text_from_csv,
        'text/plain': extract_text_from_file,
        'image/png': extract_text_from_image,
        'image/jpg': extract_text_from_image,
        'image/jpeg': extract_text_from_image
    }
    if file_type in extraction_functions:
        logger.info("======= {} =======".format(file_type))
        text_extraction_function = extraction_functions[file_type]
        text = text_extraction_function(file_path)
        extracted_text=text
        return text
    else:
        logger.error("Unsupported file type:", file_type)
        return None