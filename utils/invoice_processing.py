"""
Filename: invoice_processing.py
Author: Deepak Nigam
Date created: 2024-06-05
License: MIT License
Description: This file contains invoice processing related functions.
"""

from config.config import openai_client, openai_gpt_model
from utils.image_processing import extract_text_from_image
import fitz
import mimetypes
import pandas as pd
from docx import Document
import csv

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
        print("======= {} =======".format(file_type))
        text_extraction_function = extraction_functions[file_type]
        text = text_extraction_function(file_path)
        extracted_text=text
        return text
    else:
        print("Unsupported file type:", file_type)
        return None

def fetch_invoice_details(text):
    prompt='''You are developing a data extraction system that needs to parse information from various documents, including invoices. You need to extract specific details from the provided text and output them in a structured JSON format.

    Context/Text:

    [Provide the context/text you want the model to extract information from. Include sample invoice information. If given text is empty or doesn't contain the required information, do not add anything from your end.]

    Instructions:
    Format:
    Strictly adhere to the following format for your final response. Please extract the following details and organize them into a JSON format:

    Invoice Number
    Invoice Date
    Due Date
    Balance Amount
    Due Amount
    Paid To
    Ensure that the JSON format is structured appropriately, with each detail clearly labeled.

    '''+ text

    # Call Chat Completion API
    response = openai_client.chat.completions.create(model=openai_gpt_model, messages=[{"role": "user", "content": prompt}])
    # Display AI assistant's response
    print(response.choices[0].message.content)
