from pinecone import ServerlessSpec
from langchain.chains import RetrievalQA 
from langchain_pinecone import PineconeVectorStore
from pinecone import ServerlessSpec
from utils.general import load_doc, chunk_data, delete_file_from_local
from utils.gcp import download_file_from_gcp
from utils.preprocessing import clean_up_text
from utils.preprocessing import extract_text_from_pdf
from config.config import pinecone_client, openai_client, openai_embeddings, openai_llm, gcp_bucket_name, local_download_path, DB_SCHEMA, DB_SCHEMA_QUERY
from db_schema import db_schema
from langchain_core.documents import Document

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

def build_pinecone_db_schema_index():
    document = [Document(page_content=db_schema, metadata={"source": DB_SCHEMA})]

    pinecone_client.create_index(
        name=DB_SCHEMA,
        dimension=1536,
        metric="cosine",
        spec=ServerlessSpec(
            cloud='aws',
            region='us-east-1'
        )
    )

    PineconeVectorStore.from_documents(document, openai_embeddings, index_name=DB_SCHEMA)

    index = pinecone_client.Index(DB_SCHEMA)
    index.describe_index_stats()

    print("====Success=======")

def get_sql_query_context(index_name, query):
    client = openai_client
    res = client.embeddings.create(
        input=[query],
        model='text-embedding-3-small'
    )
    index = pinecone_client.Index(index_name)
    xq = res.data[0].embedding
    res = index.query(vector=xq, top_k=10, include_metadata=True)
    contexts = [item['metadata']['text'] for item in res['matches']]
    return contexts[0]