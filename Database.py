import mysql.connector
from mysql.connector import Error

# db_name = 'library_db'
# user = 'root'
# host = '127.0.0.1'
# password = 'jeweller-zipper-reck2'


class Database:
    def __init__(self, host, user, password, db_name):
        self.connection = None
        try:
            self.connection = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=db_name
            )
            self.cursor = self.connection.cursor()
            print("Connected to the database")
        except Error as e:
            print(f"Error: '{e}'")

    def execute_query(self, query, params=None):
        try:
            self.cursor.execute(query, params)
            self.connection.commit()
            return self.cursor.lastrowid
        except Error as e:
            print(f"Error: '{e}'")
            return None

    def fetch_query(self, query, params=None):
        try:
            self.cursor.execute(query, params)
            result = self.cursor.fetchall()
            return result
        except Error as e:
            print(f"Error: '{e}'")
            return []  # Return an empty list on error

    def close(self):
        if self.connection.is_connected():
            self.cursor.close()
            self.connection.close()
            print("Connection closed.")
