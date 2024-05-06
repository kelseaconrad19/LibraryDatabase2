class Genre:
    def __init__(self, name, database, description, category):
        self.name = name
        self.database = database
        self.description = description
        self.category = category

    def save_new_genre(self):
        query = "INSERT INTO genres (name, description, category) VALUES (%s, %s, %s)"
        params = (self.name, self.description, self.category)
        self.database.execute_query(query, params)
        print(f"{self.name} added to the genres.")

    def delete_genre(self):
        query = "DELETE FROM genres WHERE name = %s"
        self.database.execute_query(query, (self.name,))
        print(f"{self.name} deleted.")

    @staticmethod
    def display_genre_info(name, db):
        query = "SELECT * FROM genres WHERE name = %s"
        genre = db.fetch_query(query, (name,))
        if genre:
            genre = genre[0]
            print(f"\nName: {genre[1]}\nDescription: {genre[2]}\nCategory: {genre[3]}\n")
        else:
            print("Genre not found.")

    @staticmethod
    def display_all_genres(db):
        query = "SELECT * FROM genres"
        genres = db.fetch_query(query)
        if genres:
            for genre in genres:
                print(f"\nName: {genre[1]}\nDescription: {genre[2]}\nCategory: {genre[3]}\n")
        else:
            print("No genres found.")

    @staticmethod
    def get_genre_by_name(name, db):
        query = "SELECT * FROM genres WHERE name = %s"
        genre = db.fetch_query(query, (name,))
        if genre:
            genre = genre[0]
            return Genre(name=genre[1], database=db, description=genre[2], category=genre[3])
        else:
            return None
