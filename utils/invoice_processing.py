"""
Filename: invoice_processing.py
Author: Deepak Nigam
Date created: 2024-06-05
License: MIT License
Description: This file contains invoice processing related functions.
"""

from config.config import openai_client, openai_gpt_model
import json

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
    invoice_details = json.loads(response.choices[0].message.content)
    return invoice_details
