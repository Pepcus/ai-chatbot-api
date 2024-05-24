"""
Filename: app.py
Author: Deepak Nigam
Date created: 2024-04-28
License: MIT License
Description: Entry point of the app, contains API implementation.
"""

from fastapi import FastAPI, Header
from pydantic import BaseModel
from utils.pinecone_vectorstore import build_pinecone_index
from utils.chat import get_chat_response
from auth import is_authorized_request

app = FastAPI()

class Message(BaseModel):
    role: str
    content: str

@app.get('/')
def hello_world():
    return "Hello,World"

@app.get("/api/response")
def get_response(query: str, company: str, chat_id: str, authorization: str = Header(None, convert_underscores=True)):
    print("=======inside get_response===========")
    is_authorized_request(auth=authorization)
    response = get_chat_response(chat_id, company, query)
    return response

@app.post("/api/pinecone/index/{company}")
def create_index(company: str, authorization: str = Header(None, convert_underscores=True)):
    is_authorized_request(auth=authorization)
    build_pinecone_index(company)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app)