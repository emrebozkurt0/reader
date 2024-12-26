from main.utils.get_data import fill_table

class Authors:
    def __init__(self, connection, fill=False):
        self.columns = [
            "author_id", 
            "author_name", 
            "gender", 
            "about", 
            "img_url", 
            "country_id"
        ]
        self.connection = connection
        fill_table(
            self.connection, 
            './data/authors_countries.csv', 
            self.columns, 
            'Authors',
            fill=fill
        )

    def add(self, author_data):
        try:
            cursor = self.connection.cursor()

            required_fields = ['author_name', 'country_id']
            for field in required_fields:
                if field not in author_data or not author_data[field]:
                    raise ValueError(f"Missing or invalid field: {field}")
            
            fields = ', '.join(self.columns[1:])
            placeholders = ', '.join(['%s'] * (len(self.columns) - 1))
            query = f"INSERT INTO Authors ({fields}) VALUES ({placeholders})"
            values = tuple(author_data.get(col) for col in self.columns[1:])

            cursor.execute(query, values)
            self.connection.commit()
            cursor.close()
            print(f"Added author: {values}")
        except Exception as e:
            print(f"Error adding author: {e}")

    def update(self, author_id, data):
        try:
            cursor = self.connection.cursor()

            update_clauses = ', '.join([f"{col} = %s" for col in data.keys()])
            query = f"UPDATE authors SET {update_clauses} WHERE author_id = %s"
            values = list(data.values()) + [author_id]

            cursor.execute(query, values)
            self.connection.commit()
            cursor.close()
            print(f"Author {author_id} updated with: {data}")
        except Exception as e:
            print(f"Error updating author {author_id}: {e}")

    def delete(self, author_id):
        try:
            cursor = self.connection.cursor()
            query = "DELETE FROM authors WHERE author_id = %s"
            cursor.execute(query, (author_id,))
            self.connection.commit()
            cursor.close()
            print(f"Author {author_id} has been deleted.")
        except Exception as e:
            print(f"Error deleting author {author_id}: {e}")

    def search(self, filters):
        try:
            cursor = self.connection.cursor()

            conditions = []
            values = []
            for field, value in filters.items():
                if value is not None:
                    conditions.append(f"{field} LIKE %s")
                    values.append(f"%{value}%")
            where_clause = " AND ".join(conditions) if conditions else "1=1"

            query = f"SELECT * FROM Authors WHERE {where_clause}"
            cursor.execute(query, tuple(values))
            results = cursor.fetchall()
            cursor.close()

            print(f"Found {len(results)} authors matching filters: {filters}")
            return results
        except Exception as e:
            print(f"Error searching authors: {e}")
            return []

    def filter_by_gender(self, gender=None):
        try:
            cursor = self.connection.cursor()

            conditions = []
            values = []
            if gender is not None:
                conditions.append("gender = %s")
                values.append(gender)
            where_clause = " AND ".join(conditions) if conditions else "1=1"

            query = f"SELECT * FROM Authors WHERE {where_clause}"
            cursor.execute(query, tuple(values))
            results = cursor.fetchall()
            cursor.close()

            print(f"Filtered authors by gender={gender}")
            return results
        except Exception as e:
            print(f"Error filtering authors by gender: {e}")
            return []

    def filter_by_country(self, country_id=None):
        try:
            cursor = self.connection.cursor()

            conditions = []
            values = []
            if country_id is not None:
                conditions.append("country_id = %s")
                values.append(country_id)
            where_clause = " AND ".join(conditions) if conditions else "1=1"

            query = f"SELECT * FROM Authors WHERE {where_clause}"
            cursor.execute(query, tuple(values))
            results = cursor.fetchall()
            cursor.close()

            print(f"Filtered authors by country_id={country_id}")
            return results
        except Exception as e:
            print(f"Error filtering authors by country_id: {e}")
            return []

    def get_by_id(self, id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM authors WHERE author_id = %s", (id,))
        result = cursor.fetchone()
        cursor.close()
        if result:
            return {
                "author_id": result[0],
                "author_name": result[1],
                "gender": result[2],
                "about": result[3],
                "img_url": result[4],
                "country_id": result[5],
            }
        else:
            return None
    