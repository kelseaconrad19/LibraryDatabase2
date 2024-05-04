from mysql.connector import Error


class Member:
    def __init__(self, name=None, library_card_id=None, fines=None, db=None):
        self.__name = name
        self.__library_card_id = library_card_id
        self.fines = fines
        self.db = db

    def get_name(self):
        return self.__name

    @staticmethod
    def get_by_library_id(library_id, db):
        query = 'SELECT * FROM users WHERE library_id = %s'
        result = db.fetch_query(query, (library_id,))
        return result

    def save_member(self):
        try:
            query = 'INSERT INTO users (name, library_id, fines) VALUES (%s, %s, %s)'
            params = (self.__name, self.__library_card_id, self.fines)
            self.__library_card_id = self.db.execute_query(query, params)
        except Error as e:
            print(f"Error: '{e}'")

    def delete_member(self):
        query = 'DELETE FROM users WHERE library_id = %s'
        self.db.execute_query(query, (self.__library_card_id,))
        return f"{self.__name} deleted."

    @staticmethod
    def display_member_info(library_id, db):
        query = 'SELECT * FROM users WHERE library_id = %s'
        params = (library_id,)
        results = db.fetch_query(query, params)
        if results:
            results = results[0]
            return f"\nName: {results[1]}\n Library Card ID: {results[2]}\n Fines: ${results[3]}\n"
        else:
            return "Member not found."

    @staticmethod
    def display_all_members(db):
        query = "SELECT * FROM users"
        members = db.fetch_query(query)
        if members:
            for member in members:
                print(f"\nName: {member[1]}\n Library Card ID: {member[2]}\n Fines: ${member[3]}\n")
        else:
            print("No members found.")


