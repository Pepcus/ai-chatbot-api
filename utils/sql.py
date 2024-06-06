"""
Filename: sql.py
Author: Deepak Nigam
Date created: 2024-06-06
License: MIT License
Description: This file contains SQL related functions.
"""
from db_con import conn
from utils.logs import logger

def execute_query(query, params=None):
    try:
        logger.info("Connection open")
        # Create a cursor object
        cur = conn.cursor()

        # Execute the query
        if params:
            cur.execute(query, params)
        else:
            cur.execute(query)

        results = []
        # Fetch all results (if it's a SELECT query)
        if query.strip().lower().startswith('select'):
            results = cur.fetchall()

        # Commit the transaction (for INSERT, UPDATE, DELETE queries)
        if query.strip().lower().startswith(('insert', 'update', 'delete')):
            conn.commit()

        # Close the cursor and connection
        cur.close()
        logger.info("Connection closed")
        return results

    except Exception as e:
        logger.error(f"An error occurred: {e}")