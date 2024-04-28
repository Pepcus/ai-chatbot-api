
from fastapi import FastAPI, File, UploadFile, Form
from langchain_openai import OpenAIEmbeddings
from pinecone.grpc import PineconeGRPC
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_community.utilities import SQLDatabase
from utils_langchain_pinecone import build_pinecone_index
from utils_langchain_chat import get_chat_response
from utils_langchain_general import delete_file_from_local
import time
import os

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
    return response

@app.post("/index/{company}")
def create_index(company: str):
    build_pinecone_index(pc, embeddings, bucket_name, company)

@app.post("/api/response")
async def process_data(
    query: str = Form(...),
    company: str = Form(...),
    file: UploadFile = File(...)
):
    # Process the file, query, and company data here
    try:
        if (file):
            file_name = str(time.time()) + file.filename
            file_location = os.environ['LOCAL_DOWNLOAD_PATH'] + file_name
            with open(file_location, "wb") as f:
                f.write(await file.read())
            query = query + ' from the document ' + file_location
            response = get_chat_response(pc, db, llm, embeddings, company, query)
            delete_file_from_local(file_name)
        else:
            response = get_chat_response(pc, db, llm, embeddings, company, query)

        return response
    except Exception as e:
        return e

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app)