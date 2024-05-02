from langchain_openai import OpenAIEmbeddings
from pinecone.grpc import PineconeGRPC
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_community.utilities import SQLDatabase
from openai import OpenAI
import os

load_dotenv()

openai_api_key = os.environ['OPENAI_API_KEY']
openai_gpt_model = 'gpt-3.5-turbo'
openai_client = OpenAI()
openai_embeddings = OpenAIEmbeddings(api_key=os.environ['OPENAI_API_KEY'])
pinecone_client = PineconeGRPC(api_key=os.environ['PINECONE_API_KEY'])
openai_llm = ChatOpenAI(  
        openai_api_key=os.environ['OPENAI_API_KEY'],
        model_name='gpt-3.5-turbo',  
        temperature=0.0  
    )
pg_database = SQLDatabase.from_uri(os.environ['PG_DB_URI'])
gcp_bucket_name = os.environ['GCP_BUCKET_NAME']
pg_db_uri = os.environ['PG_DB_URI']
api_client_id = os.environ['API_CLIENT_ID']
api_client_secret = os.environ['API_CLIENT_SECRET']

SQL_SYSTEM_PROMPT = '''Generate SQL based on the given context and user query. Given final query to run don't give any additional suffix or prefix.'''