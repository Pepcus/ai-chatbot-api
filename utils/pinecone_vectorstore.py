from pinecone import ServerlessSpec
from langchain_pinecone import PineconeVectorStore
from utils.general import load_doc, chunk_data, delete_file_from_local
from utils.gcp import download_file_from_gcp
from utils.preprocessing import clean_up_text
from utils.preprocessing import extract_text_from_pdf
from config.config import pinecone_client, openai_client, openai_embeddings, openai_llm, gcp_bucket_name, local_download_path, DB_SCHEMA
from db_schema import db_schema
from langchain_core.documents import Document
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain

def build_pinecone_index(index_name):

    file_name = index_name + ".pdf"
    download_file_from_gcp(gcp_bucket_name, file_name)

    docs=load_doc(local_download_path + file_name)
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

    delete_file_from_local(file_name)
    print("====Success=======")

def get_pinecone_query_engine(index_name):
    system_prompt = (
        "You are an assistant for question-answering tasks. "
        "Use the following pieces of retrieved context to answer "
        "the question. If you don't know the answer, say that you "
        "don't know."
        "\n\n"
        "{context}"
    )

    assistant_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            ("human", "{input}"),
        ]
    )

    question_answer_chain = create_stuff_documents_chain(openai_llm, assistant_prompt)
    index = pinecone_client.Index(index_name.swapcase())
    text_field = "text"

    vectorstore = PineconeVectorStore(
        index, openai_embeddings, text_field
    )

    return create_retrieval_chain(vectorstore.as_retriever(), question_answer_chain)


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