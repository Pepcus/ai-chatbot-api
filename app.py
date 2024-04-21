from fastapi import FastAPI
import utils
import os
import openai
from llama_index.core import SimpleDirectoryReader
from llama_index.llms.openai import OpenAI
from llama_index.core import Document
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.vector_stores.pinecone import PineconeVectorStore
from pinecone import Pinecone, ServerlessSpec
from IPython.display import Markdown, display
from utils import build_sentence_window_index
from utils import get_sentence_window_query_engine

app = FastAPI()
openai.api_key = utils.get_openai_api_key()
llm = OpenAI(model="gpt-3.5-turbo", temperature=0.1)
pc = Pinecone(api_key=os.environ['PINECONE_API_KEY'])


documents = SimpleDirectoryReader(
    input_files=["./documents/999.pdf"]
).load_data()

document = Document(text="\n\n".join([doc.text for doc in documents]))

print(type(documents), "\n")
print(len(documents), "\n")
print(type(documents[0]))
print(documents[0])


@app.get('/')
def hello_world():
    return "Hello,World"

@app.get("/response/")
async def get_response(query: str, company: str):
    index_name = company + '-handbook'
    sentence_window_engine = get_sentence_window_query_engine(index_name)
    window_response = sentence_window_engine.query(query)
    print(window_response.response)
    return (window_response.response)

@app.post("/index/{company}")
async def create_index(company: str):
    index_name = company + '-handbook'
    index = build_sentence_window_index(document, llm,  index_name, "local:BAAI/bge-small-en-v1.5")
    return "Success"

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app)