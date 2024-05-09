from pinecone import ServerlessSpec
from langchain.chains import RetrievalQA 
from langchain_pinecone import PineconeVectorStore
from pinecone import ServerlessSpec
from utils_langchain_general import load_doc, chunk_data, delete_file_from_local
from utils_langchain_gcp import download_file_from_gcp
from utils_langchain_preprocessing import clean_up_text
from utils_langchain_preprocessing import extract_text_from_pdf
from app_config import pinecone_client, openai_embeddings, openai_llm, gcp_bucket_name, local_download_path

def build_pinecone_index(index_name):

    file_name = index_name + ".pdf"
    text_file_name = index_name + ".txt"
    text_file_path = local_download_path + text_file_name
    download_file_from_gcp(gcp_bucket_name, file_name)

    #Extract text from pdf
    extracted_text = extract_text_from_pdf(local_download_path+file_name)

    #PreProcessing 1 - Cleaning up the extracted_text data
    cleaned_data = clean_up_text(extracted_text)

    #Writing the cleaned extracted_text data into a text file
    with open(text_file_path, "w", encoding = 'utf-8') as f:
        f.write(cleaned_data)

    docs=load_doc(local_download_path)
    print(len(docs))

    documents=chunk_data(docs=docs)
    print(len(documents))

    index_name = index_name.swapcase()
    pinecone_client.create_index(
        name=index_name,
        dimension=1536,
        metric="cosine",
        spec=ServerlessSpec(
            cloud='aws',
            region='us-east-1'
        )
    )

    # Store in DB and retrieve it
    PineconeVectorStore.from_documents(documents, openai_embeddings, index_name=index_name)

    index = pinecone_client.Index(index_name)
    index.describe_index_stats()

    delete_file_from_local(text_file_name)
    delete_file_from_local(file_name)
    print("====Success=======")

def get_pinecone_query_engine(index_name):
    index_name = index_name.swapcase()
    index = pinecone_client.Index(index_name)
    text_field = "text"

    vectorstore = PineconeVectorStore(
        index, openai_embeddings, text_field
    )
    qa = RetrievalQA.from_chain_type(
        llm=openai_llm,  
        chain_type="stuff",
        retriever=vectorstore.as_retriever()
    )

    return qa