from fastapi import FastAPI
import utils_llamaindex
import os
from llama_index.embeddings.openai import OpenAIEmbedding
from pinecone.grpc import PineconeGRPC
from utils_llamaindex import build_pinecone_index, get_pinecone_query_engine
from pathlib import Path
from llama_index.core import download_loader

app = FastAPI()
pc = PineconeGRPC(api_key=os.environ['PINECONE_API_KEY'])
embeddings=OpenAIEmbedding(api_key=os.environ['OPENAI_API_KEY'])

PDFReader = download_loader("PDFReader")
loader = PDFReader()

@app.get('/')
def hello_world():
    return "Hello,World"

@app.get("/response/")
async def get_response(query: str, company: str):
    index_name = company + '-handbook'
    query_engine = get_pinecone_query_engine(pc, index_name)
    query_response = query_engine.query(query)
    print(query_response.response)
    return (query_response.response)

@app.post("/index/{index}")
async def create_index(index: str):
    documents = loader.load_data(file=Path('./documents/999.pdf'))

    print(type(documents), "\n")
    print(len(documents), "\n")
    print(type(documents[0]))
    print(documents[0])

    index_name = index + '-handbook'
    build_pinecone_index(pc, documents,  index_name, embeddings)
    return "Success"

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app)