from main.utils.get_data import fill_table

class Countries:
    def __init__(self, connection, fill=False):
        self.columns = [
            "country_id", 
            "country_name",
            "country_region"
        ]
        self.connection = connection
        fill_table(
            self.connection, 
            './data/authors_countries.csv', 
            self.columns, 
            'Countries',
            fill=fill
        )


    