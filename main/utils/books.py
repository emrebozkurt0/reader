class Books:
    def __init__(self, connection):
        self.columns = ["book_id", "isbn", "title", "author_id", "publication_year", "publisher_id"]
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

    