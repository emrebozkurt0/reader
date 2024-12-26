from main.utils.get_data import fill_table

class Comments:
    def __init__(self, connection, fill=False):
        self.columns = [
            "comment_id", 
            "book_id", 
            "comment_datetime", 
            "user_id", 
            "content", 
            "score"
        ] 
        self.connection = connection
        fill_table(
            self.connection, 
            './data/comments.csv', 
            self.columns, 
            'Comments',
            fill=fill
        )

    def add(self, comment_data):
        try:
            cursor = self.connection.cursor()

            required_fields = ['user_id', 'content', 'book_id']
            
            cursor.execute("SELECT COUNT(*) FROM Books WHERE book_id = %s", (comment_data['book_id'],))
            if cursor.fetchone()[0] == 0:
                raise ValueError(f"book_id {comment_data['book_id']} does not exist in the Books table.")

            for field in required_fields:
                if field not in comment_data or not comment_data[field]:
                    raise ValueError(f"Missing or invalid field: {field}")
            for field, value in comment_data.items():
                if value in [None, '', 'None']:
                    comment_data[field] = None

            fields = ', '.join(self.columns[1:])
            placeholders = ', '.join(['%s'] * (len(self.columns) - 1))
            query = f"INSERT INTO comments ({fields}) VALUES ({placeholders})"
            values = tuple(comment_data.get(col) for col in self.columns[1:])


            cursor.execute(query, values)
            self.connection.commit()
            cursor.close()
            print(f"Added comment: {values}")
        except Exception as e:
            print(f"Error adding comment: {e}")

    def update(self, comment_id, updates):
        try:
            cursor = self.connection.cursor()

            update_clauses = ', '.join([f"{col} = %s" for col in updates.keys()])
            query = f"UPDATE comments SET {update_clauses} WHERE comment_id = %s"
            values = list(updates.values()) + [comment_id]

            cursor.execute(query, values)
            self.connection.commit()
            cursor.close()
            print(f"Comment {comment_id} updated with: {updates}")
        except Exception as e:
            print(f"Error updating comment {comment_id}: {e}")

    def delete(self, comment_id):
        try:
            cursor = self.connection.cursor()
            query = "DELETE FROM comments WHERE comment_id = %s"
            cursor.execute(query, (comment_id,))
            self.connection.commit()
            cursor.close()
            print(f"Comment {comment_id} has been deleted.")
        except Exception as e:
            print(f"Error deleting comment {comment_id}: {e}")

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

            query = f"SELECT * FROM comments WHERE {where_clause}"
            cursor.execute(query, tuple(values))
            results = cursor.fetchall()
            cursor.close()

            print(f"Found {len(results)} comments matching filters: {filters}")
            return results
        except Exception as e:
            print(f"Error finding comments: {e}")
            return []

    def filter_by_score(self, min_score=None, max_score=None):
        try:
            cursor = self.connection.cursor()

            conditions = []
            values = []
            if min_score is not None:
                conditions.append("score >= %s")
                values.append(min_score)
            if max_score is not None:
                conditions.append("score <= %s")
                values.append(max_score)
            where_clause = " AND ".join(conditions) if conditions else "1=1"

            query = f"SELECT * FROM comments WHERE {where_clause}"
            cursor.execute(query, tuple(values))
            results = cursor.fetchall()
            cursor.close()

            print(f"Filtered comments by score: min={min_score}, max={max_score}")
            return results
        except Exception as e:
            print(f"Error filtering comments by score: {e}")
            return []

    def get_top_comments(self, limit=5):
        try:
            cursor = self.connection.cursor()
            query = f"SELECT * FROM comments ORDER BY score DESC LIMIT %s"
            cursor.execute(query, (limit,))
            results = cursor.fetchall()
            cursor.close()
            print(f"Retrieved top {limit} comments by score.")
            return results
        except Exception as e:
            print(f"Error retrieving top comments: {e}")
            return []

    def get_by_id(self, id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM comments WHERE comment_id = %s", (id,))
        result = cursor.fetchone()
        cursor.close()
        if result:
            return {
                "comment_id": result[0],
                "book_id": result[1],
                "comment_datetime": result[2],
                "user_id": result[3],
                "content": result[4],
                "score": result[5],
            }
        else:
            return None
