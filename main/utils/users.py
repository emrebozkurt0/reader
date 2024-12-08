import csv

class Users:
    def __init__(self, connection):
        self.columns = ["user_id", "name", "email", "username", "date_of_birth", "gender", "subscription_id"]
        self.connection = connection

    def fill(self, csv_file_path):
        try:
            with open(csv_file_path, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file, delimiter=";")

                cursor = self.connection.cursor()
                for row in reader:
                    columns = ', '.join(self.columns)
                    placeholders = ', '.join(['%s'] * len(self.columns))  
                    sql = f"INSERT INTO Users ({columns}) VALUES ({placeholders})"
                    values = [row[column] for column in self.columns]
                    cursor.execute(sql, values)

                self.connection.commit()
                print("Data successfully inserted into the database.")

        except Exception as e:
            print(f"Error occurred: {e}")
            self.connection.rollback()

    def add(self):
        pass

    def update(self):
        pass

    def delete(self):
        pass
        
    def search(self):
        pass

    def filter(self):
        pass

    