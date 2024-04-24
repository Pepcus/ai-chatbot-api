from dotenv import load_dotenv
from pinecone import ServerlessSpec
from langchain.chains import RetrievalQA 
from langchain_pinecone import Pinecone
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_pinecone import PineconeVectorStore
from pinecone import ServerlessSpec

load_dotenv()

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

def build_pinecone_index(pc, embeddings, index_name):
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

def get_pinecone_query_engine(pc, llm, embeddings, index_name, query):
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
    return qa