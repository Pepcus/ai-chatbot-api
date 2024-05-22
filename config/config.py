"""
Filename: config.py
Author: Deepak Nigam
Date created: 2024-04-28
License: MIT License
Description: This file contains application configuration.
"""

from langchain_openai import OpenAIEmbeddings
from pinecone import Pinecone
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from openai import OpenAI
import os

load_dotenv()

openai_api_key = os.environ['OPENAI_API_KEY']
openai_gpt_model = 'gpt-3.5-turbo'
openai_client = OpenAI()
openai_embeddings = OpenAIEmbeddings(api_key=os.environ['OPENAI_API_KEY'])
pinecone_client = Pinecone(api_key=os.environ['PINECONE_API_KEY'])
openai_llm = ChatOpenAI(  
        openai_api_key=os.environ['OPENAI_API_KEY'],
        model_name='gpt-3.5-turbo',  
        temperature=0.0  
    )
gcp_bucket_name = os.environ['GCP_BUCKET_NAME']
api_client_id = os.environ['API_CLIENT_ID']
api_client_secret = os.environ['API_CLIENT_SECRET']
local_download_path = os.environ['LOCAL_DOWNLOAD_PATH']

#AIML-17
LANGCHAIN_API_KEY = os.environ['LANGCHAIN_API_KEY']
LANGCHAIN_TRACING_V2 = os.environ['LANGCHAIN_TRACING_V2']
LANGCHAIN_ENDPOINT= os.environ['LANGCHAIN_ENDPOINT'] 
LANGCHAIN_PROJECT = os.environ['LANGCHAIN_PROJECT'] 