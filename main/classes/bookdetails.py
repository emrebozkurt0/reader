from main.utils.get_data import fill_table

class BookDetails:
    def __init__(self, connection, fill=False):
        self.columns = [
            "book_details_id",
            "book_id",
            "rating",
            "language",
            "page_number",
            "counts_of_review"
        ]
        self.connection = connection
        fill_table(
            self.connection, 
            './data/book_and_details.csv', 
            self.columns, 
            'BookDetails',
            fill=fill
        )