from langchain_community.agent_toolkits import create_sql_agent
from langchain_openai import ChatOpenAI
from langchain_community.utilities import SQLDatabase
from config import openai_llm, pg_database

agent_executor = create_sql_agent(
                    llm=openai_llm, 
                    db=pg_database,
                    agent_type="openai-tools"
                )

def get_sql_query_agent(query):
    return agent_executor.invoke(query)