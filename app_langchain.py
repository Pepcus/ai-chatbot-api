from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import Pinecone
from langchain_pinecone import PineconeVectorStore
from pinecone import ServerlessSpec
from pinecone.grpc import PineconeGRPC
from dotenv import load_dotenv
from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI  
from langchain.chains import RetrievalQA 
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

## Read the document
def read_doc(directory):
    file_loader=PyPDFDirectoryLoader(directory)
    documents=file_loader.load()
    return documents

## Divide the docs into chunks
### https://api.python.langchain.com/en/latest/text_splitter/langchain.text_splitter.RecursiveCharacterTextSplitter.html#
def chunk_data(docs,chunk_size=800,chunk_overlap=50):
    text_splitter=RecursiveCharacterTextSplitter(chunk_size=chunk_size,chunk_overlap=chunk_overlap)
    doc=text_splitter.split_documents(docs)
    return docs

def get_index_name(company):
    return company + "-handbook"

@app.get("/response/")
def get_response(query: str, company: str):
    index_name = get_index_name(company)

    index = pc.Index(index_name)
    text_field = "text"

    vectorstore = Pinecone(
        index, embeddings, text_field
    )

    vectorstore.similarity_search(  
        query,  # our search query  
        k=3  # return 3 most relevant docs  
    )  
   
    qa = RetrievalQA.from_chain_type(  
        llm=llm,  
        chain_type="stuff",
        retriever=vectorstore.as_retriever()  
    )
    response = qa.invoke(query)
    return response

@app.post("/index/{index}")
def create_index(index: str):
    index_name = get_index_name(index)

    pc.create_index(
        name=index_name,
        dimension=1536,
        metric="cosine",
        spec=ServerlessSpec(
            cloud='aws',
            region='us-east-1'
        )
    )
 
    doc=read_doc('documents/')
    len(doc)

    documents=chunk_data(docs=doc)
    len(documents)

    # Store in DB and retrieve it
    PineconeVectorStore.from_documents(documents, embeddings, index_name=index_name)

    index = pc.Index(index_name)
    index.describe_index_stats()
    print()

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app)