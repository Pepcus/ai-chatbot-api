from app_config import openai_gpt_model, openai_client, SQL_SYSTEM_PROMPT, SQL_ANSWER_PROMPT, pg_db_uri
from langchain_community.utilities import SQLDatabase
from utils_langchain_pinecone import get_sql_query_context
from app_config import DB_SCHEMA, DB_SCHEMA_QUERY

db_schema_context = get_sql_query_context(DB_SCHEMA, DB_SCHEMA_QUERY)

# Create a function to generate SQL
def generate_sql(query, company):
    response = openai_client.chat.completions.create(
            model=openai_gpt_model,
            messages=[
                {"role": "system", "content": SQL_SYSTEM_PROMPT},
                {"role": "user", "content": "context: "+ db_schema_context +", Query: " +query +",  company: "+ company}
            ]
    )
    print(response.choices[0].message.content)
    return response.choices[0].message.content

def execute_query(query):
    print("=======going to execute below query===========", query)
    db = SQLDatabase.from_uri(pg_db_uri)
    return db.run(query)

def generate_and_execute_sql_query(query, company):
    sql_query = generate_sql(query, company)
    result = execute_query(sql_query)

    response = openai_client.chat.completions.create(
        model=openai_gpt_model,
        messages=[
            {"role": "system", "content": SQL_ANSWER_PROMPT},
            {"role": "user", "content": "Question: "+ query +",   Answer:" + result }
        ]
    )
    print(response.choices[0].message.content)
    return response.choices[0].message.content