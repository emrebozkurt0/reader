from main.utils.get_data import fill_table

class Publishers:
    def __init__(self, connection):
        self.columns = [
            "publisher_id", 
            "publisher_name"
        ]
        self.connection = connection
        fill_table(
            self.connection, 
            './data/book_and_details.csv', 
            self.columns, 
            'Publishers'
        )

    def add(self, data):
        cursor = self.connection.cursor()
        query = f"""
        INSERT INTO publishers ({', '.join(self.columns[1:])})
        VALUES (%s)
        """
        values = (
            data["publisher_name"],
        )
        try:
            cursor.execute(query, values)
            self.connection.commit()
        except Exception as e:
            self.connection.rollback()
            print("Error:", e)
        finally:
            cursor.close()
        

    def update(self):
        pass

    def delete(self):
        pass
        
    def search(self):
        pass

    def filter(self):
        pass

    