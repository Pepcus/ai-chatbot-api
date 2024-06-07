"""
Filename: app.py
Author: Deepak Nigam
Date created: 2024-04-28
License: MIT License
Description: Entry point of the app, contains API implementation.
"""

from fastapi import FastAPI, Header,File,UploadFile
from pydantic import BaseModel
from utils.pinecone_vectorstore import build_pinecone_index
from utils.chat import get_chat_response
from auth import is_authorized_request
import shutil
from pathlib import Path
from fastapi.middleware.cors import CORSMiddleware
from utils.general import get_file_type,extract_text_based_on_file_type
from utils.invoice_processing import fetch_invoice_details
from config.config import UPLOAD_DIR,ALLOW_ORIGINS,ALLOW_HEADERS,ALLOW_CREDENTIALS,ALLOW_METHODS


app = FastAPI()

# Define the directory to store uploaded files
UPLOAD_DIR = UPLOAD_DIR
UPLOAD_DIR.mkdir(exist_ok=True)
# This example allows all origins, adjust as needed for production
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOW_ORIGINS,  # In production, replace "*" with the actual origins
    allow_credentials=ALLOW_CREDENTIALS,
    allow_methods=ALLOW_METHODS,  # Make sure to allow the methods you use
    allow_headers=ALLOW_HEADERS,
)

class Message(BaseModel):
    role: str
    content: str

@app.get('/')
def hello_world():
    return "Hello,World"

@app.get("/api/response")
def get_response(query: str, company: str, chat_id: str, authorization: str = Header(None, convert_underscores=True)):
    is_authorized_request(auth=authorization)
    response = get_chat_response(chat_id, company, query)
    return response

@app.post("/api/pinecone/index/{company}")
def create_index(company: str, authorization: str = Header(None, convert_underscores=True)):
    is_authorized_request(auth=authorization)
    build_pinecone_index(company)

@app.post("/api/invoice")
def upload_invoice(file: UploadFile = File(...),authorization: str = Header(None, convert_underscores=True)):
    
    is_authorized_request(auth=authorization)
    #Configuring the upload path
    file_path = UPLOAD_DIR / file.filename
    #Creating the file using file object and storing it 
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    file_type=get_file_type(file.filename)
    text=extract_text_based_on_file_type(file_type,file_path)

    invoice_details=fetch_invoice_details(text)
    return {
        "filename": file.filename,
        "invoiceNumber": invoice_details.get("invoice_number"),
        "invoiceDate": invoice_details.get("invoice_date"),
        "dueDate": invoice_details.get("due_date"),
        "balanceAmount": invoice_details.get("balance_amount"),
        "dueAmount": invoice_details.get("due_amount"),
        "paidTo": invoice_details.get("paid_to"),
        "message": "File successfully uploaded and stored."
    }

@app.post("/api/invoice/accept")
def accept_invoice(authorization: str = Header(None, convert_underscores=True)):
    # Authorization check
    is_authorized_request(auth=authorization)

    return {"message": "Invoice changes accepted."}
    

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app)