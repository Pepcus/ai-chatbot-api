"""
Filename: sql.py
Author: Deepak Nigam
Date created: 2024-06-06
License: MIT License
Description: This file contains SQL related functions.
"""

from langchain_community.utilities import SQLDatabase
from config.config import pg_db_uri

def execute_query(query):
    print("=======going to execute below query===========", query)
    db = SQLDatabase.from_uri(pg_db_uri)
    return db.run(query)
