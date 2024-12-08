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

    def update(self):
        pass

    def delete(self):
        pass

    def search(self):
        pass

    def filter(self):
        pass
