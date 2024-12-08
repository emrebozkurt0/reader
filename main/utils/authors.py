class Authors:
    def __init__(self, connection):
        self.columns = ["author_id", "name", "gender", "about", "img_url", "country_id"]
        self.connection = connection

    def primary_key_generator(self):
        pass

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

    