from app_config import openai_gpt_model, openai_client, pg_db_uri
from langchain_community.utilities import SQLDatabase
from db_schema import db_schema

SQL_SYSTEM_PROMPT='''You are a postgres SQL expert. Given an input question, creat a syntactically correct postgres SQL query to run. Unless the user specifies in the question a specific number of examples to obtain, query for at most 10 results using the LIMIT clause as per {dialect}. You can order the results to return the most informative data in the database. Never query for all columns from a table. You must query only the columns that are needed to answer the question. Wrap each column name in double quotes to denote them as delimited identifiers. Pay attention to use only the column names you can see in the tables below. Be careful to not query for columns that do not exist. Also, pay attention to which column is in which table. Pay attention to use date('now') function to get the current date, if the question involves 'today'. Write an initial draft of the query. 

Then double check the postgres SQL query for common mistakes, including: 
- Using NOT IN with NULL values - Using UNION when UNION ALL should have been used 
- Using BETWEEN for exclusive ranges - Data type mismatch in predicates 
- Properly quoting identifiers 
- Using the correct number of arguments for functions 
- Casting to the correct data type 
- Using the proper columns for joins 

Must to follow things:
- Do not use the 'users' table for quering.
- Do not add any prefix or suffix to the SQL query. 
- Give clean SQL query ready to run on database.
- Always use LOWER function to convert the strings and and lower function to data before comparing.
- Always give your final response in the following format only: {query}
'''

# Create a function to generate SQL
def generate_sql(query):
    response = openai_client.chat.completions.create(
            model=openai_gpt_model,
            messages=[
                {"role": "system", "content": SQL_SYSTEM_PROMPT},
                {"role": "user", "content": "context: "+ db_schema +", Query: " + query}
            ]
    )
    print(response.choices[0].message.content)
    return response.choices[0].message.content

def execute_query(query):
    print("=======going to execute below query===========", query)
    db = SQLDatabase.from_uri(pg_db_uri)
    return db.run(query)

def generate_and_execute_sql_query(query):
    sql_query = generate_sql(query)
    result = execute_query(sql_query)
    return result