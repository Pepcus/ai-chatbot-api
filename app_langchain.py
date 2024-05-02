
from fastapi import FastAPI, Header
from utils_langchain_pinecone import build_pinecone_index
from utils_langchain_chat import get_chat_response
from auth import is_authorized_request

app = FastAPI()

@app.get('/')
def hello_world():
    return "Hello,World"

@app.get("/api/response")
def get_response(query: str, company: str, authorization: str = Header(None, convert_underscores=True)):
    is_authorized_request(auth=authorization)
    response = get_chat_response(company, query)
    return response

@app.post("/api/pinecone/index/{company}")
def create_index(company: str, authorization: str = Header(None, convert_underscores=True)):
    is_authorized_request(auth=authorization)
    build_pinecone_index(company)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app)