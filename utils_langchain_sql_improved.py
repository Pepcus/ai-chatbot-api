from app_config import openai_gpt_model, openai_client, SQL_SYSTEM_PROMPT, openai_api_key, pg_db_uri
from langchain_community.utilities import SQLDatabase
from db_schema import db_schema

# Create a function to generate SQL
def generate_sql(query):
    response = openai_client.chat.completions.create(
            model=openai_gpt_model,
            messages=[
                {"role": "system", "content": SQL_SYSTEM_PROMPT},
                {"role": "user", "content": "context: "+ db_schema +",   Query:" +query}
            ]
    )
    print(response.choices[0].message.content)
    return response.choices[0].message.content

def execute_query(query):
    db = SQLDatabase.from_uri(pg_db_uri)
    return db.run(query)

def generate_and_execute_sql_query(query):
    sql_query = generate_sql(query)
    result = execute_query(sql_query)

    response = openai_client.chat.completions.create(
        model=openai_gpt_model,
        messages=[
            {"role": "system", "content": "Generate user friendly message from the given question and answer. Be specific as per the question and don't give any additional information."},
            {"role": "user", "content": "Question: "+ query +",   Answer:" + result }
        ]
    )
    print(response.choices[0].message.content)
    return response.choices[0].message.content