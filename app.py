
from fastapi import FastAPI, Header
from pydantic import BaseModel
from utils.pinecone import build_pinecone_index, build_pinecone_db_schema_index
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
    is_authorized_request(auth=authorization)
    response = get_chat_response(chat_id, company, query)
    return response

@app.post("/api/pinecone/index/{company}")
def create_index(company: str, authorization: str = Header(None, convert_underscores=True)):
    is_authorized_request(auth=authorization)
    build_pinecone_index(company)

@app.post("/api/pinecone/db_schema_index")
def create_db_schema_index(authorization: str = Header(None, convert_underscores=True)):
    is_authorized_request(auth=authorization)
    build_pinecone_db_schema_index()

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app)