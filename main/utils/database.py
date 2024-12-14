import mysql.connector
from ..config import db_host, db_user, db_password

def get_connection():
    connection = mysql.connector.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        auth_plugin='mysql_native_password'
    )
    cursor = connection.cursor()
    cursor.execute('USE reader')
    return connection
