from ..config import db_host, db_user, db_password, db_name  
import mysql.connector

def get_mysql_data_types(column_type):
    mysql_types = {
        3: 'INT',
        253: 'VARCHAR',
        252: 'TEXT',
        12: 'DATETIME',
        254: 'CHAR',
        13: 'YEAR',
        2: 'SMALLINT',
        246: 'DECIMAL',
        10: 'DATE'
    }
    
    return mysql_types.get(column_type, 'UNKNOWN')

def get_table_data(table_name):
    connection = mysql.connector.connect(host=db_host, database=db_name, user=db_user, password=db_password)    
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM {table_name}")
    columns = cursor.description
    centers = cursor.fetchall()
    cursor.close()
    connection.close()
    column_types = []
    for column in columns: 
        column_name = column[0]
        column_type = column[1]
        mysql_data_type = get_mysql_data_types(column_type)
        item = {'column_name': column_name, 'column_type': mysql_data_type}
        column_types.append(item)
    return centers 