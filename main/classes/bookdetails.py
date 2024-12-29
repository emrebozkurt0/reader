from main.utils.get_data import fill_table


class BookDetails:
    def __init__(self, connection, fill=False):
        self.columns = [
            "book_details_id",
            "book_id",
            "rating",
            "language",
            "page_number",
            "counts_of_review",
        ]
        self.connection = connection
        fill_table(
            self.connection,
            "./data/book_and_details.csv",
            self.columns,
            "BookDetails",
            fill=fill,
        )

    def get_by_id(self, id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM BookDetails WHERE book_id = %s", (id,))
        result = cursor.fetchone()
        cursor.close()
        if result:
            return {
                "book_details_id": result[0],
                "book_id": result[1],
                "rating": result[2],
                "language": result[3],
                "page_number": result[4],
                "counts_of_review": result[5],
            }
        else:
            return None
