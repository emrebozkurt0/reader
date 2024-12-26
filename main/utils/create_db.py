import mysql.connector
from database import get_connection
from main.classes.authors import Authors
from main.classes.comments import Comments  
from main.classes.publishers import Publishers
from main.classes.users import Users
from main.classes.books import Books
from main.classes.countries import Countries

def create_database(connection):
    try:
        cursor = connection.cursor()
        cursor.execute(f"SHOW DATABASES LIKE 'reader'")
        result = cursor.fetchone()
        if result:
            cursor.execute(f"DROP DATABASE reader")
        cursor.execute(f"CREATE DATABASE reader")
        print(f"Database 'reader' created.")
        cursor.execute('USE reader')
    except mysql.connector.Error as err:
        print(f"Error while creating database: {err}")
    finally:
        if connection.is_connected():
            cursor.close()

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

def initialize_database(connection):
    try:
        cursor = connection.cursor()

        sql_files = [
            './table_queries/users_subscription.sql',
            './table_queries/authors_countries.sql',
            './table_queries/books_bookdetails_publishers.sql',
            './table_queries/comments.sql',
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

def fill_tables(connection):
    try:
        Users(connection)
        Countries(connection)
        Authors(connection)
        Publishers(connection)
        Books(connection)
        Comments(connection)

    except mysql.connector.Error as err:
        print(f"Error while filling comments table: {err}")

if __name__ == "__main__":
    try:
        connection = get_connection()
        create_database(connection)
        initialize_database(connection)
        fill_tables(connection)

        if connection.is_connected():
            connection.close()

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
