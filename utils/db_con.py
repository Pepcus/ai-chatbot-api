import psycopg2
from config.config import db_name, db_user, db_password, db_host, db_port

conn_params = {
    "dbname": db_name,
    "user": db_user,
    "password": db_password,
    "host": db_host,
    "port": db_port
}
# Establish the connection
conn = psycopg2.connect(**conn_params)