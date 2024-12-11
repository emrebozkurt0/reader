from main.utils.get_data import fill_table

class Users:
    def __init__(self, connection):
        self.columns = [
            "user_id", 
            "name", 
            "email", 
            "username", 
            "date_of_birth", 
            "gender", 
            "subscription_id"
        ]
        self.connection = connection
        fill_table(
            self.connection, 
            './data/users_subscription.csv', 
            self.columns, 
            'Users'
        )

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

    