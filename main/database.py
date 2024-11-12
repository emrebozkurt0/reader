import mysql.connector
import os

def get_db_connection():
    return mysql.connector.connect(
        host="your_host",
        user="your_user",
        password="your_password",
        database="your_database"
    )

def load_sql_query(filename):
    path = os.path.join("table_queries", filename)
    with open(path, 'r') as file:
        query = file.read()
    return query
