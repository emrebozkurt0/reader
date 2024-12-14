from main.utils.get_data import fill_table

class Books:
    def __init__(self, connection):
        self.columns = [
            "book_id",
            "isbn",
            "title",
            "author_id",
            "publication_year",
            "publisher_id",
        ]
        self.connection = connection
        fill_table(
            self.connection, 
            './data/book_and_details.csv', 
            self.columns, 
            'Books'
        )


    def add(self, data):
        cursor = self.connection.cursor()
        query = f"""
        INSERT INTO books ({', '.join(self.columns[1:])})
        VALUES (%s, %s, %s, %s, %s)
        """
        values = (
            data["isbn"],
            data["title"],
            data["author_id"],
            data["publication_year"],
            data["publisher_id"],
        )
        try:
            cursor.execute(query, values)
            self.connection.commit()
        except Exception as e:
            self.connection.rollback()
            print("Error:", e)
        finally:
            cursor.close()

    def update(self,data,id):
        cursor = self.connection.cursor()
        query = f"""
        UPDATE books SET isbn = %s, title = %s, author_id = %s, publication_year = %s, publisher_id = %s WHERE book_id = %s
        """
        values = (
            data["isbn"],
            data["title"],
            data["author_id"],
            data["publication_year"],
            data["publisher_id"],
            id
        )
        try:
            cursor.execute(query, values)
            self.connection.commit()
        except Exception as e:
            self.connection.rollback()
            print("Error:", e)
        finally:
            cursor.close()

    def delete(self,id):
        cursor = self.connection.cursor()
        query = "DELETE FROM books WHERE book_id = %s"
        values = (id,)
        try:
            cursor.execute(query, values)
            self.connection.commit()
        except Exception as e:
            self.connection.rollback()
            print("Error:", e)
        finally:
            cursor.close()

    def search(self):
        pass

    def filter(self):
        pass

    def get_by_id(self, id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM books WHERE book_id = %s", (id,))
        result = cursor.fetchone()
        cursor.close()
        if result:
            return {
                "id": result[0],
                "isbn": result[1],
                "title": result[2],
                "author_id": result[3],
                "publication_year": result[4],
                "publisher_id": result[5],
            }
        else:
            return None