from fastapi import FastAPI
import utils
import os
from llama_index.embeddings.openai import OpenAIEmbedding
from pinecone.grpc import PineconeGRPC
from utils import build_pinecone_index, get_pinecone_query_engine
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

@app.get("/pinecone-response/")
async def get_response(query: str, company: str):
    index_name = company + '-handbook'
    sentence_window_engine = get_pinecone_query_engine(pc, index_name)
    window_response = sentence_window_engine.query(query)
    print(window_response.response)
    return (window_response.response)

@app.post("/pinecone-index/{index}")
async def create_pinecone_index(index: str):
    documents = loader.load_data(file=Path('./documents/999.pdf'))

    print(type(documents), "\n")
    print(len(documents), "\n")
    print(type(documents[0]))
    print(documents[0])

    index_name = index + '-handbook'
    index = build_pinecone_index(pc, documents,  index_name, embeddings)
    return "Success"

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app)