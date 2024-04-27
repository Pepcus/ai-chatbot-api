
from langchain_openai import OpenAIEmbeddings
from pinecone.grpc import PineconeGRPC
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_community.utilities import SQLDatabase
from utils_langchain_pinecone import build_pinecone_index
from utils_langchain_chat import get_chat_response
import os
from fastapi import FastAPI

app = FastAPI()

load_dotenv()

## Embedding Technique Of OPENAI
embeddings=OpenAIEmbeddings(api_key=os.environ['OPENAI_API_KEY'])
pc = PineconeGRPC(api_key=os.environ['PINECONE_API_KEY'])
llm = ChatOpenAI(  
        openai_api_key=os.environ['OPENAI_API_KEY'],
        model_name='gpt-3.5-turbo',  
        temperature=0.0  
    )
db = SQLDatabase.from_uri(os.environ['PG_DB_URI'])
bucket_name = os.environ['GCP_BUCKET_NAME']

@app.get('/')
def hello_world():
    return "Hello,World"

@app.get("/response/")
def get_response(query: str, company: str):
    response = get_chat_response(pc, db, llm, embeddings, company, query)
    resp = response['output']
    print("=======response from API==========", resp)
    return resp

@app.post("/index/{company}")
def create_index(company: str):
    build_pinecone_index(pc, embeddings, bucket_name, company)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app)