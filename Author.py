class Author:
    def __init__(self, db=None, name=None, bio=None, author_id=None):
        self.db = db
        self.name = name
        self.biography = bio
        self.author_id = author_id

    def save_author(self):
        if self.author_id is None:
            # Insert new author
            query = "INSERT INTO authors (name, biography) VALUES (%s, %s)"
            params = (self.name, self.biography)
            self.author_id = self.db.execute_query(query, params) # retrieve the new author's id
        else:
            # Update existing author
            query = "UPDATE authors SET name = %s, biography = %s WHERE id = %s"
            params = (self.name, self.biography, self.author_id)
            self.db.execute_query(query, params)

    def delete_author(self):
        query = "DELETE FROM authors WHERE id = %s"
        self.db.execute_query(query, (self.author_id,))
        return f"{self.name} deleted."

    def get_author(self):
        """Get the author's information. Used to display the author's information."""
        query = "SELECT * FROM authors WHERE id = %s"
        author = self.db.fetch_query(query, (self.author_id,))
        return author[0] if author else None

    @staticmethod
    def get_by_id(author_id, db):
        query = "SELECT id, name, biography FROM authors WHERE id = %s"
        params = (author_id,)
        results = db.fetch_query(query, params)
        if results:
            results = results[0]
            return Author(author_id=results[0], name=results[1], bio=results[2], db=db)

    @staticmethod
    def get_by_name(name, db):
        query = "SELECT id, name, biography FROM authors WHERE name = %s"
        params = (name,)
        results = db.fetch_query(query, params)
        if results:
            results = results[0]
            return Author(author_id=results[0], name=results[1], bio=results[2], db=db)
