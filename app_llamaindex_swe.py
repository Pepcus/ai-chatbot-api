from fastapi import FastAPI
import utils_llamaindex_swe
import os
from dotenv import load_dotenv
from llama_index.embeddings.openai import OpenAIEmbedding
from utils_llamaindex_swe import build_sentence_window_index, get_sentence_window_query_engine
from llama_index.llms.openai import OpenAI
from llama_index.core import SimpleDirectoryReader
from pinecone import Pinecone
from llama_index.core import Document

load_dotenv()

app = FastAPI()
pc = Pinecone(api_key=os.environ['PINECONE_API_KEY'])
embeddings=OpenAIEmbedding(api_key=os.environ['OPENAI_API_KEY'])
llm = OpenAI(
        openai_api_key=os.environ['OPENAI_API_KEY'],  
        model_name='gpt-3.5-turbo',  
        temperature=0.0  
    )

@app.get('/')
def hello_world():
    return "Hello,World"

@app.get("/response/")
async def get_response(query: str, company: str):
    index_name = company + '-handbook'
    query_engine = get_sentence_window_query_engine(pc, index_name)
    query_response = query_engine.query(query)
    print(query_response.response)
    return (query_response.response)

@app.post("/index/{index}")
async def create_index(index: str):
    documents = SimpleDirectoryReader("./documents").load_data()
    #document = Document(text="\n\n".join([doc.text for doc in documents]))
    index_name = index + '-handbook'
    build_sentence_window_index(pc, documents, llm, embeddings, index_name)
    return "Success"

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app)