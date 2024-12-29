from main.utils.get_data import fill_table
from flask import flash

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
            flash("Author added successfully.", "success")
            print(f"Added author: {values}")
        except Exception as e:
            flash("Author cannot be added.", "error")
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
            flash("Author updated successfully.", "success")
            print(f"Author {author_id} updated with: {data}")
        except Exception as e:
            flash("Author cannot be added.", "error")
            print(f"Error updating author {author_id}: {e}")

    def delete(self, author_id):
        try:
            cursor = self.connection.cursor()
            query = "DELETE FROM authors WHERE author_id = %s"
            cursor.execute(query, (author_id,))
            self.connection.commit()
            cursor.close()
            flash("Author deleted successfully.", "success")
            print(f"Author {author_id} has been deleted.")
        except Exception as e:
            flash("Author cannot be deleted.", "error")
            print(f"Error deleting author {author_id}: {e}")

    def search(self, filters):
        cursor = self.connection.cursor()
        conditions = []
        values = []
        join_query = """
            SELECT a.author_id, a.author_name, a.gender, a.about, a.img_url, c.country_name
            FROM Authors a
            LEFT JOIN Countries c ON a.country_id = c.country_id
        """

        for column, value in filters.items():
            if value: 
                if column == "country_name":
                    conditions.append("c.country_name LIKE %s")
                    values.append(f"%{value}%")
                else:
                    conditions.append(f"{column} LIKE %s")
                    values.append(f"%{value}%")
        
        query = join_query
        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        try:
            cursor.execute(query, values)
            results = cursor.fetchall()
            return results
        except Exception as e:
            print("Error during search:", e)
            return []
        finally:
            cursor.close()


    def get_top_authors(self, limit=100):
        try:
            cursor = self.connection.cursor()

            query = """
                SELECT 
                    a.author_id, 
                    a.author_name, 
                    ROUND(AVG(bd.rating), 2) AS average_rating
                FROM 
                    Authors a
                JOIN 
                    Books b ON a.author_id = b.author_id
                JOIN 
                    BookDetails bd ON b.book_id = bd.book_id
                GROUP BY 
                    a.author_id
                HAVING 
                    COUNT(b.book_id) > 1
                ORDER BY 
                    average_rating DESC
                LIMIT %s;
            """
            cursor.execute(query, (limit,))
            results = cursor.fetchall()
            cursor.close()

            print(f"Retrieved top {limit} authors by average rating.")
            return results
        except Exception as e:
            print(f"Error occurred while fetching the top {limit} authors: {e}")
            return []

    def get_most_reviewed_female_authors(self, limit=100):
        try:
            cursor = self.connection.cursor()

            query = """
                SELECT
                    a.author_name,
                    SUM(bd.counts_of_review) AS total_reviews
                FROM 
                    Authors a
                JOIN 
                    Books b ON a.author_id = b.author_id
                JOIN 
                    BookDetails bd ON b.book_id = bd.book_id
                WHERE 
                    a.gender = 'Female'
                GROUP BY 
                    a.author_id, a.author_name
                ORDER BY 
                    total_reviews DESC
                LIMIT %s;
            """

            cursor.execute(query, (limit,))
            results = cursor.fetchall()
            cursor.close()

            print(f"Retrieved top {limit} most reviewed female authors.")
            return results
        except Exception as e:
            print(f"Error occurred while fetching the most reviewed female authors: {e}")
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
    