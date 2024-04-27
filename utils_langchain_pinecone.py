from dotenv import load_dotenv
from pinecone import ServerlessSpec
from langchain.chains import RetrievalQA 
from langchain_pinecone import PineconeVectorStore
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain.agents import initialize_agent
from pinecone import ServerlessSpec
from utils_langchain_general import read_doc, chunk_data, delete_file_from_local
from utils_langchain_gcp import download_file_from_gcp
from langchain.agents import Tool
from openai import OpenAI
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
        llm=llm,
        max_iterations=3,
        early_stopping_method='generate',
        memory=conversational_memory
    )

    return agent.invoke(query)

def get_pinecone_chat_completion_query_engine(pc, llm, embeddings, index_name, query):
    client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])
    res = client.embeddings.create(
        input=[query],
        model='text-embedding-3-small'
    )
    index_name = index_name.swapcase()
    index = pc.Index(index_name)
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