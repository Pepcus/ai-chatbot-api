
from fastapi import FastAPI
from utils_langchain_pinecone import build_pinecone_index
from utils_langchain_chat import get_chat_response

app = FastAPI()

@app.get('/')
def hello_world():
    return "Hello,World"

@app.get("/api/response")
def get_response(query: str, company: str):
    response = get_chat_response(company, query)
    return response

@app.post("/api/pinecone/index/{company}")
def create_index(company: str):
    build_pinecone_index(company)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app)