"""
Filename: invoice_processing.py
Author: Deepak Nigam
Date created: 2024-06-05
License: MIT License
Description: This file contains invoice processing related functions.
"""
from utils.logs import logger
from config.config import openai_client, openai_gpt_model
import json

def fetch_invoice_details(text):
    prompt='''

    You are developing a data extraction system that needs to parse information from various documents, including invoices. You need to extract specific details from the provided text and output them in a structured JSON format.

    Context/Text:
    [Provide the context/text you want the model to extract information from. Include sample invoice information. If the given text is empty or doesn't contain the required information, do not add anything from your end.]

    Instructions:
    Format:
    Strictly adhere to the following format for your final response. Please extract the following details and organize them into a JSON format:

    invoice_number
    invoice_date
    due_date
    balance_amount
    due_amount
    paid_to
    Ensure that the JSON format is structured appropriately, with each detail clearly labeled. If you don't have a value for any particular field, use 'NA' as the default value. Do not make up values from your end.

    Examples:
    1. When all values are available:

    output json
    {
        "invoice_number": "INV123456",
        "invoice_date": "2024-06-01",
        "due_date": "2024-07-01",
        "balance_amount": "1500.00",
        "due_amount": "1500.00",
        "paid_to": "ABC Corp"
    }

    2. When few values are missing:
    
    output json
    {
        "invoice_number": "INV123457",
        "invoice_date": "2024-06-02",
        "due_date": "NA",
        "balance_amount": "2000.00",
        "due_amount": "NA",
        "paid_to": "XYZ Ltd"
    }

    '''+ text

    # Call Chat Completion API
    response = openai_client.chat.completions.create(model=openai_gpt_model, messages=[{"role": "user", "content": prompt}])
    # Display AI assistant's response
    logger.info(response.choices[0].message.content)
    invoice_details = json.loads(response.choices[0].message.content)
    return invoice_details
