from langchain_community.agent_toolkits import create_sql_agent
from langchain_openai import ChatOpenAI
from langchain_community.utilities import SQLDatabase
import os

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
db = SQLDatabase.from_uri(os.environ['PG_DB_URI'])

agent_executor = create_sql_agent(llm, db=db, agent_type="openai-tools")

def get_sql_query_agent(query):
    return agent_executor.invoke(query)