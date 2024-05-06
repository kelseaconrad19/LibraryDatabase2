from datetime import datetime, timedelta
from member import Member


class Book:
    def __init__(self, title, author_id, isbn, genre_id, member_id, db):
        self.db = db
        self.title = title
        self.author = author_id
        self.ISBN = isbn
        self.genre = genre_id
        self.availability = True
        self.member = member_id

    def save_book(self):
        query = 'INSERT INTO books (isbn, title, author_id, genre_id, availability, member) VALUES (%s, %s, %s, %s, %s, %s)'
        params = (self.ISBN, self.title, self.author, self.genre, self.availability, self.member)
        self.ISBN = self.db.execute_query(query, params)

    @staticmethod
    def get_by_title(title, db):
        query = 'SELECT * FROM books WHERE title = %s'
        params = (title,)
        results = db.fetch_query(query, params)
        if results:
            results = results[0]
            return Book(title=results[1], author_id=results[2], isbn=results[0], genre_id=results[3], member_id=results[5], db=db)

    def check_out_book(self, member_id):
        if self.availability:
            self.set_availability(False)
            # member = Member.get_by_library_id(member_id, self.db)
            self.member = member_id
            query = 'UPDATE books SET availability = %s, member = %s WHERE isbn = %s'
            params = (self.availability, member_id, self.ISBN)
            self.db.execute_query(query, params)
            user_id = Member.get_by_library_id(member_id, self.db)
            # add book to borrowed books table
            query = 'INSERT INTO borrowed_books (book_isbn, user_id, borrow_date, return_date) VALUES (%s, %s, %s, %s)'
            borrowed_date = datetime.now().strftime('%Y-%m-%d')
            return_date = (datetime.now() + timedelta(days=14)).strftime('%Y-%m-%d')
            params = (self.ISBN, user_id, borrowed_date, return_date)
            self.db.execute_query(query, params)
            print(f"{self.title} has been borrowed. It is due on {return_date}.")
        else:
            raise Exception(f"{self.title} is not available.")

    def check_if_overdue(self):
        query = 'SELECT return_date FROM borrowed_books WHERE book_isbn = %s AND user_id = %s'
        params = (self.ISBN, self.member)
        return_date = self.db.fetch_query(query, params)
        if return_date:
            return_date = return_date[0][0]
            current_date = datetime.now().strftime('%Y-%m-%d')
            current_date = datetime.strptime(current_date, '%Y-%m-%d')
            return_date = datetime.strptime(return_date, '%Y-%m-%d')
            if current_date > return_date:
                days_overdue = (current_date - return_date).days
                fine_per_day = 2
                fine = fine_per_day * days_overdue
                query = 'UPDATE users SET fines = fines + %s WHERE library_id = %s'
                params = (fine, self.member)
                self.db.execute_query(query, params)
                print(f"You have been fined ${fine} for late return.")
            else:
                print("The return date is in the future.")
        else:
            print("No return date found for the book.")

    def return_book(self, member_id):
        # check if the book is borrowed by the member
        user_id = Member.get_by_library_id(member_id, self.db)
        print(f"user_id: {user_id}, self.member: {self.member}")  # Debugging line
        # if self.member == user_id:
        #     # check if the book is overdue
        #     self.check_if_overdue()
        #     self.set_availability(True)
        #     self.remove_from_borrowed_books(member_id)
        #     self.member = 'None'
        #     self.update_book_after_return()
        #     print(f"{self.title} has been returned.")
        # else:
        #     print(f"{self.title} is not borrowed by {member_id}. User id: {user_id}")

    def set_availability(self, availability):
        self.availability = availability

    def update_book_after_return(self):
        query = 'UPDATE books SET availability = %s, member = %s WHERE isbn = %s'
        params = (self.availability, self.member, self.ISBN)
        self.db.execute_query(query, params)

    def update_book(self):
        query = 'UPDATE books SET title = %s, author_id = %s, genre_id = %s, availability = %s, member = %s WHERE isbn = %s'
        params = (self.title, self.author, self.genre, self.availability, self.member, self.ISBN)
        self.db.execute_query(query, params)

    def remove_from_borrowed_books(self, member_id):
        query = 'DELETE FROM borrowed_books WHERE book_isbn = %s AND user_id = %s'
        params = (self.ISBN, member_id)
        self.db.execute_query(query, params)

    @staticmethod
    def display_all_books(db):
        query = """
        SELECT books.title, authors.name, books.isbn, genres.name, users.name, books.member
        FROM books
        INNER JOIN authors ON books.author_id = authors.id
        INNER JOIN genres ON books.genre_id = genres.id
        INNER JOIN users ON books.member = users.id
        """
        books = db.fetch_query(query)
        if books:
            for book in books:
                if book[5] == '1':
                    availability = 'Available'
                    print(f"Title: {book[0]}\nAuthor: {book[1]}\nISBN: {book[2]}\nGenre: {book[3]}\nAvailability: {availability}\nMember: {book[4]}\n")
                else:
                    availability = 'Not Available'
                    print(f"Title: {book[0]}\nAuthor: {book[1]}\nISBN: {book[2]}\nGenre: {book[3]}\nAvailability: {availability}\nMember: {book[4]}\n")
        else:
            print("No books found.")
