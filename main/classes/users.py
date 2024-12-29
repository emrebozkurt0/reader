from textwrap import fill
from main.utils.get_data import fill_table
from flask import flash

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
            "role",
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
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        values = (
            data["name"],
            data["email"],
            data["username"],
            data["date_of_birth"],
            data["gender"],
            data["subscription_id"],
            data["role"]
        )
        try:
            cursor.execute(query, values)
            self.connection.commit()
            flash("User added successfully.","success")
        except Exception as e:
            flash("User cannot be added.","error")
            print(query)
            self.connection.rollback()
            print("Error:", e)
        finally:
            cursor.close()

    def update(self,data,id):
        cursor = self.connection.cursor()
        query = f"""
        UPDATE users SET name = %s, email = %s, username = %s, date_of_birth = %s, gender = %s, subscription_id = %s, role = %s WHERE user_id = %s
        """
        values = (
            data["name"],
            data["email"],
            data["username"],
            data["date_of_birth"],
            data["gender"],
            data["subscription_id"],
            data["role"],
            id
        )
        try:
            cursor.execute(query, values)
            self.connection.commit()
            flash("User updated successfully.","success")
        except Exception as e:
            flash("User cannot be updated.","error")
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
            flash("User deleted successfully.","success")
        except Exception as e:
            flash("User cannot be deleted.","error")
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
                "role": result[8]
            }
        else:
            return None

    def get_top_users(self, limit=100):
        try:
            cursor = self.connection.cursor()

            query = """
                SELECT 
                    u.user_id, 
                    u.name, 
                    u.username, 
                    u.email, 
                    SUM(c.score) AS total_score
                FROM 
                    Users u
                LEFT JOIN 
                    Comments c ON u.user_id = c.user_id
                GROUP BY 
                    u.user_id
                ORDER BY 
                    total_score DESC
                LIMIT %s;
            """
            cursor.execute(query, (limit,))
            results = cursor.fetchall()
            cursor.close()

            print(f"Retrieved top {limit} users by total comment score.")
            return results
        except Exception as e:
            print(f"Error occurred while fetching the top {limit} users: {e}")
            return []