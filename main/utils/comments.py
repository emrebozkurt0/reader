class Comments:
    def __init__(self, connection):
        self.columns = ["comment_id", "comment_date", "user_id", "reference_id", "content", "score"]
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

    