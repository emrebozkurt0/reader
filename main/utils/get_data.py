import csv
from main.utils.database import get_connection

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

def get_table_data(table_name, sort_column=None):
    connection = get_connection()
    cursor = connection.cursor()
    
    try:
        query = f"SELECT * FROM {table_name}"
        if sort_column:
            query += f" ORDER BY {sort_column}"
        
        cursor.execute(query)
        centers = cursor.fetchall()
        return centers
    finally:
        cursor.close()
        connection.close()


def fill_table(connection, file_path, column_names, table_name, fill=True):
    if (fill):
        try:
            with open(file_path, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file, delimiter=';')

                cursor = connection.cursor()
                ids = []
                id = 'country_id' if table_name == 'Countries' else table_name[:-1].lower() + '_id'
                for row in reader:
                    if row[id] in ids:
                        continue
                    columns = ', '.join(column_names)
                    placeholders = ', '.join(['%s'] * len(column_names))
                    sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
                    values = [row[column] if row[column] != '' else None for column in column_names]
                    cursor.execute(sql, values)
                    ids.append(row[id])

                connection.commit()
                print(f"{table_name} data successfully inserted into the database.")

        except Exception as e:
            print(f"Error occurred: {e} {table_name}")
            connection.rollback()
