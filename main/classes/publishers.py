from main.utils.get_data import fill_table
from flask import flash

class Publishers:
    def __init__(self, connection, fill=False):
        self.columns = ["publisher_id", "publisher_name"]
        self.connection = connection
        fill_table(
            self.connection, "./data/book_and_details.csv", self.columns, "Publishers", fill=fill
        )

    def add(self, data):
        cursor = self.connection.cursor()
        query = f"""
        INSERT INTO publishers ({', '.join(self.columns[1:])})
        VALUES (%s)
        """
        values = (data["publisher_name"],)
        try:
            cursor.execute(query, values)
            self.connection.commit()
            flash("Publisher added successfully.","success")
        except Exception as e:
            flash("Publisher cannot be added.","error")
            self.connection.rollback()
            print("Error:", e)
        finally:
            cursor.close()

    def update(self,data,id):
        cursor = self.connection.cursor()
        query = f"""
        UPDATE publishers SET publisher_name = %s WHERE publisher_id = %s
        """
        values = (data["publisher_name"], id)
        try:
            cursor.execute(query, values)
            self.connection.commit()
            flash("Publisher updated successfully.","success")
        except Exception as e:
            flash("Publisher cannot be updated.","error")
            self.connection.rollback()
            print("Error:", e)
        finally:
            cursor.close()

    def delete(self,id):
        cursor = self.connection.cursor()
        query = "DELETE FROM publishers WHERE publisher_id = %s"
        try:
            cursor.execute(query, (id,))
            self.connection.commit()
            flash("Publisher deleted successfully.","success")
        except Exception as e:
            flash("Publisher cannot be deleted.","error")
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
        cursor.execute("SELECT * FROM publishers WHERE publisher_id = %s", (id,))
        result = cursor.fetchone()
        cursor.close()
        if result:
            return {
                "id": result[0],
                "publisher_name": result[1],
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
        query = "SELECT * FROM publishers"
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