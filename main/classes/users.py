from textwrap import fill
from main.utils.get_data import fill_table

class Users:
    def __init__(self, connection, fill=False):
        self.columns = [
            "user_id", 
            "name", 
            "email", 
            "username", 
            "date_of_birth", 
            "gender", 
            "subscription_id", 
            "password"
        ]
        self.connection = connection
        fill_table(
            self.connection, 
            './data/users_subscription.csv', 
            self.columns, 
            'Users',
            fill=fill
        )

    def add(self, data):
        cursor = self.connection.cursor()
        query = f"""
            INSERT INTO users ({', '.join(self.columns[1:-1])})
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        values = (
            data["name"],
            data["email"],
            data["username"],
            data["date_of_birth"],
            data["gender"],
            data["subscription_id"]
        )
        try:
            cursor.execute(query, values)
            self.connection.commit()
        except Exception as e:
            print(query)
            self.connection.rollback()
            print("Error:", e)
        finally:
            cursor.close()

    def update(self,data,id):
        cursor = self.connection.cursor()
        query = f"""
        UPDATE users SET name = %s, email = %s, username = %s, date_of_birth = %s, gender = %s, subscription_id = %s WHERE user_id = %s
        """
        values = (
            data["name"],
            data["email"],
            data["username"],
            data["date_of_birth"],
            data["gender"],
            data["subscription_id"],
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
        query = "DELETE FROM users WHERE user_id = %s"
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
        cursor.execute("SELECT * FROM users WHERE user_id = %s", (id,))
        result = cursor.fetchone()
        cursor.close()
        if result:
            return {
                "user_id": result[0],
                "name": result[1],
                "email": result[2],
                "username": result[3],
                "date_of_birth": result[5],
                "gender": result[6],
                "subscription_id": result[7],
            }
        else:
            return None

    