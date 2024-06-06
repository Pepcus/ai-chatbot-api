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
import json
import tempfile

load_dotenv()
gcp_bucket_name = os.environ['GCP_BUCKET_NAME']
openai_api_key = os.environ['OPENAI_API_KEY']
openai_gpt_model = 'gpt-3.5-turbo'
openai_client = OpenAI()
openai_embeddings = OpenAIEmbeddings(api_key=openai_api_key)
pinecone_client = Pinecone(api_key=os.environ['PINECONE_API_KEY'])
openai_llm = ChatOpenAI(  
        openai_api_key=openai_api_key,
        model_name='gpt-3.5-turbo',  
        temperature=0.0  
    )
api_client_id = os.environ['API_CLIENT_ID']
api_client_secret = os.environ['API_CLIENT_SECRET']
local_download_path = os.environ['LOCAL_DOWNLOAD_PATH']
pg_db_uri = os.environ['PG_DB_URI']

#AIML-17
LANGCHAIN_API_KEY = os.environ['LANGCHAIN_API_KEY']
LANGCHAIN_TRACING_V2 = os.environ['LANGCHAIN_TRACING_V2']
LANGCHAIN_ENDPOINT= os.environ['LANGCHAIN_ENDPOINT'] 
LANGCHAIN_PROJECT = os.environ['LANGCHAIN_PROJECT'] 

gcp_json = {
  "type": os.environ['GCP_TYPE'],
  "project_id": os.environ['GCP_PROJECT_ID'],
  "private_key_id": os.environ['GCP_PRIVATE_KEY_ID'],
  "private_key": os.environ['GCP_PRIVATE_KEY'],
  "client_email": os.environ['GCP_CLIENT_EMAIL'],
  "client_id": os.environ['GCP_CLIENT_ID'],
  "auth_uri": os.environ['GCP_AUTH_URI'],
  "token_uri": os.environ['GCP_TOKEN_URI'],
  "auth_provider_x509_cert_url": os.environ['GCP_AUTH_PROVIDER_X509_CERT_URL'],
  "client_x509_cert_url": os.environ['GCP_CLIENT_X509_CERT_URL'],
  "universe_domain": os.environ['GCP_UNIVERSE_DOMAIN']
}

# Create a temporary file to write the credentials JSON
with tempfile.NamedTemporaryFile(delete=False, mode='w', suffix='.json') as temp_file:
    json.dump(gcp_json, temp_file)
    temp_file_path = temp_file.name

# Set the GOOGLE_APPLICATION_CREDENTIALS environment variable to the path of the temporary file
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = temp_file_path