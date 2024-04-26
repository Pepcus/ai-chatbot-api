
from langchain_openai import OpenAIEmbeddings
from pinecone.grpc import PineconeGRPC
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_community.utilities import SQLDatabase
from utils_langchain_pinecone import get_pinecone_query_engine, build_pinecone_index
from utils_langchain_sql import get_sql_query_agent
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
def get_response(query: str, company: str, role: str):
    if (role == 'HR_ASSISTANT'):
      query_engine = get_pinecone_query_engine(pc, llm, embeddings, company, query)
      resp = query_engine.invoke(query)
      response = resp['result']
    elif (role == 'DATABASE_MASTER'):
      agent = get_sql_query_agent(db, llm)
      resp = agent.invoke({"input": query})
      response = resp['output']
    return response

@app.post("/index/{company}")
def create_index(company: str):
    build_pinecone_index(pc, embeddings, bucket_name, company)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app)