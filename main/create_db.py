import mysql.connector
from config import db_host, db_password, db_user, db_name
from utils.comments import Comments  
from utils.users import Users

def create_database():
    try:
        connection = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            auth_plugin='mysql_native_password'
        )
        cursor = connection.cursor()
        cursor.execute(f"SHOW DATABASES LIKE '{db_name}'")
        result = cursor.fetchone()
        if result:
            cursor.execute(f"DROP DATABASE {db_name}")
        cursor.execute(f"CREATE DATABASE {db_name}")
        print(f"Database '{db_name}' created.")
    except mysql.connector.Error as err:
        print(f"Error while creating database: {err}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def execute_scripts_from_file(cursor, filename):
    try:
        with open(filename, 'r') as file:
            sql_commands = file.read().split(';')
            for command in sql_commands:
                command = command.strip()
                if command:
                    try:
                        cursor.execute(command)
                    except mysql.connector.Error as err:
                        print(f"Error executing command: {command[:50]}... -> {err}")
    except FileNotFoundError:
        print(f"File not found: {filename}")
    except Exception as err:
        print(f"Error reading file {filename}: {err}")

def initialize_database():
    try:
        connection = mysql.connector.connect(
            user=db_user,
            password=db_password,
            host=db_host,
            database=db_name,
            auth_plugin='mysql_native_password'
        )
        cursor = connection.cursor()

        sql_files = [
            './table_queries/users_subscription.sql',
            './table_queries/authors_countries_comments.sql',
            './table_queries/books_bookdetails_publishers.sql'
        ]
        for sql_file in sql_files:
            execute_scripts_from_file(cursor, sql_file)

        connection.commit()
        print("Database initialized successfully with tables.")
    except mysql.connector.Error as err:
        print(f"Error while initializing database: {err}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def fill_tables():
    try:
        connection = mysql.connector.connect(
            user=db_user,
            password=db_password,
            host=db_host,
            database=db_name,
            auth_plugin='mysql_native_password'
        )
        users = Users(connection)
        comments = Comments(connection)
        users.fill('./data/users_subscription.csv')
        comments.fill('./data/comments.csv')  

    except mysql.connector.Error as err:
        print(f"Error while filling comments table: {err}")
    finally:
        if connection.is_connected():
            connection.close()

if __name__ == "__main__":
    try:
        create_database()
        initialize_database()
        fill_tables()
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
