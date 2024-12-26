from main.utils.get_data import fill_table


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
        except Exception as e:
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
        except Exception as e:
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
