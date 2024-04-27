from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient
import json
import os
from dotenv import load_dotenv

load_dotenv()

endpoint = os.environ['AZURE_API_ENDPOINT']
key = os.environ['AZURE_KEY']
model_id = os.environ['AZURE_MODEL_ID']

document_analysis_client = DocumentAnalysisClient(
    endpoint=endpoint, credential=AzureKeyCredential(key)
)

def parse_content(content):
    parsed_data = {}
    current_key = None
    current_value = ""
    keys = ["DATE", "INVOICE TO", "INVOICE NO", "ADATUM CORPORATION", "Customer Id",
            "Subtotal:", "Sales Tax:", "Total:", "SALESPERSON", "PAYMENT TERMS"]
    keys = sorted(keys, key=len, reverse=True)  # Sort keys by length to handle contained keys correctly

    lines = content.split('\n') + ["END_OF_CONTENT"]  # Add a marker to ensure last data is processed

    for line in lines:
        for key in keys:
            start_idx = line.find(key)
            if start_idx != -1:
                if current_key:
                    # Store the current data before starting the new key
                    parsed_data[current_key] = current_value.strip()
                current_key = key
                # Reset current_value to empty and skip current key in line
                current_value = line[start_idx + len(key):].strip() + " "
                # Remove the current segment from line and continue checking for more keys
                line = line[:start_idx].strip()
        
        # Append any remaining part of the line to the current value
        if current_key:
            current_value += line.strip() + " "

    # Store the last key-value pair
    if current_key:
        parsed_data[current_key] = current_value.strip()
    return parsed_data

def read_pdf_through_ocr(filelocation):
    print("====going to process file from the location ========", filelocation)
    with open(r'Invoice_10.pdf', 'rb') as file:
        binary_image_data = file.read()
        poller = document_analysis_client.begin_analyze_document(model_id, binary_image_data)

        # Make sure your document's type is included in the list of document types the custom model can analyze
        # poller = document_analysis_client.begin_analyze_document_from_url(model_id, formUrl)
        result = poller.result()
        print("Result is",result.content)
        x=parse_content(result.content)
        # Convert data to JSON format
        json_data = json.dumps(x)
    response = {}
    response['output'] = json_data
    return response