from dotenv import load_dotenv
from pinecone import ServerlessSpec
from langchain.chains import RetrievalQA 
from langchain_pinecone import PineconeVectorStore
from pinecone import ServerlessSpec
from utils_langchain_general import read_doc, chunk_data, delete_file_from_local
from utils_langchain_gcp import download_file_from_gcp
import os

load_dotenv()

def build_pinecone_index(pc, embeddings, bucket_name, index_name):

    file_name = index_name + ".pdf"
    download_file_from_gcp(bucket_name, file_name)

    doc=read_doc(os.environ['LOCAL_DOWNLOAD_PATH'])
    print(len(doc))

    documents=chunk_data(docs=doc)
    print(len(documents))

    index_name = index_name.swapcase()
    pc.create_index(
        name=index_name,
        dimension=1536,
        metric="cosine",
        spec=ServerlessSpec(
            cloud='aws',
            region='us-east-1'
        )
    )

    # Store in DB and retrieve it
    PineconeVectorStore.from_documents(documents, embeddings, index_name=index_name)

    index = pc.Index(index_name)
    index.describe_index_stats()

    delete_file_from_local(file_name)
    print("====Success=======")

def get_pinecone_query_engine(pc, llm, embeddings, index_name, query):
    index_name = index_name.swapcase()
    index = pc.Index(index_name)
    text_field = "text"

    vectorstore = PineconeVectorStore(
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