from main.utils.get_data import fill_table
from flask import flash

class Books:
    def __init__(self, connection, fill=False):
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
            'Books',
            fill=fill
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
            flash("Book added successfully.", "success")
        except Exception as e:
            flash("Book cannot be added.", "error")
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
            flash("Book updated successfully.", "success")
        except Exception as e:
            flash("Book cannot be updated.", "error")
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
            flash("Book deleted successfully.", "success")
        except Exception as e:
            flash("Book cannot be deleted.", "error")
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
    
    
    def search(self, filters):
        cursor = self.connection.cursor()
        conditions = []
        values = []

        for column, value in filters.items():
            if value: 
                conditions.append(f"{column} LIKE %s")
                values.append(f"%{value}%") 
        query = "SELECT * FROM books"
        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        try:
            cursor.execute(query, values)
            results = cursor.fetchall()
            return results
        except Exception as e:
            print("Error during search:", e)
            return []
        finally:
            cursor.close()
