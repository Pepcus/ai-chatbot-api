from dotenv import load_dotenv
from pinecone import ServerlessSpec
from langchain.chains import RetrievalQA 
from langchain_pinecone import PineconeVectorStore
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain.agents import initialize_agent
from pinecone import ServerlessSpec
from utils_langchain_general import load_doc, chunk_data, delete_file_from_local
from utils_langchain_gcp import download_file_from_gcp
from langchain.agents import Tool
from openai import OpenAI
from utils_langchain_preprocessing import clean_up_text
from utils_langchain_preprocessing import extract_text_from_pdf
from app_config import pinecone_client, openai_embeddings, openai_llm, gcp_bucket_name
import os

load_dotenv()

def build_pinecone_index(index_name):

    file_name = index_name + ".pdf"
    text_file_name = index_name + ".txt"
    text_file_path = os.environ['LOCAL_DOWNLOAD_PATH'] + text_file_name
    download_file_from_gcp(gcp_bucket_name, file_name)

    #Extract text from pdf
    extracted_text = extract_text_from_pdf(os.environ['LOCAL_DOWNLOAD_PATH']+file_name)

    #PreProcessing 1 - Cleaning up the extracted_text data
    cleaned_data = clean_up_text(extracted_text)

    #Writing the cleaned extracted_text data into a text file
    with open(text_file_path, "w", encoding = 'utf-8') as f:
        f.write(cleaned_data)

    docs=load_doc(os.environ['LOCAL_DOWNLOAD_PATH'])
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

def get_pinecone_query_engine(index_name, query):
    index_name = index_name.swapcase()
    index = pinecone_client.Index(index_name)
    text_field = "text"

    vectorstore = PineconeVectorStore(
        index, openai_embeddings, text_field
    )

    vectorstore.similarity_search(  
        query,  # our search query  
        k=3  # return 3 most relevant docs  
    )  
   
    qa = RetrievalQA.from_chain_type(
        llm=openai_llm,  
        chain_type="stuff",
        retriever=vectorstore.as_retriever()
    )

    tools = [
        Tool(
            name='Knowledge Base',
            func=qa.run,
            description=(
                'use this tool when answering general knowledge queries to get '
                'more information about the topic'
            )
        )
    ]

    # conversational memory
    conversational_memory = ConversationBufferWindowMemory(
        memory_key='chat_history',
        k=5,
        return_messages=True
    )

    agent = initialize_agent(
        agent='chat-conversational-react-description',
        tools=tools,
        llm=openai_llm,
        max_iterations=3,
        early_stopping_method='generate',
        memory=conversational_memory
    )

    return agent.invoke(query)['output']

def get_pinecone_chat_completion_query_engine(index_name, query):
    client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])
    res = client.embeddings.create(
        input=[query],
        model='text-embedding-3-small'
    )
    index_name = index_name.swapcase()
    index = pinecone_client.Index(index_name)
    xq = res.data[0].embedding
    res = index.query(vector=xq, top_k=10, include_metadata=True)
    contexts = [item['metadata']['text'] for item in res['matches']]
    augmented_query = "\n\n---\n\n".join(contexts)+"\n\n-----\n\n"+query

    primer = f"""You are Q&A bot expert in HR domain. A highly intelligent system that answers
    user questions based on the information provided by the user above
    each question. If the information can not be found in the information
    provided by the user you truthfully say "I don't know".
    """

    res = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": primer},
            {"role": "user", "content": augmented_query}
        ]
    )
    return res.choices[0].message.content.strip()