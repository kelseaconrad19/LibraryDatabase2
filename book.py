from datetime import datetime, timedelta


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

    def update_book(self):
        query = 'UPDATE books SET title = %s, author_id = %s, genre_id = %s, availability = %s, member = %s WHERE isbn = %s'
        params = (self.title, self.author, self.genre, self.availability, self.member, self.ISBN)
        self.db.execute_query(query, params)

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
            self.availability = False
            self.member = member_id

            query = 'UPDATE books SET availability = %s, member = %s WHERE isbn = %s'
            params = (self.availability, self.member, self.ISBN)
            self.db.execute_query(query, params)
            # add book to borrowed books table
            query = 'INSERT INTO borrowed_books (book_isbn, user_id, borrow_date, return_date) VALUES (%s, %s, %s, %s)'
            borrowed_date = datetime.now().strftime('%Y-%m-%d')
            return_date = (datetime.now() + timedelta(days=14)).strftime('%Y-%m-%d')
            params = (self.ISBN, self.member, borrowed_date, return_date)
            self.db.execute_query(query, params)
            print(f"{self.title} has been borrowed. It is due on {return_date}.")
        else:
            raise Exception(f"{self.title} is not available.")

    def return_book(self, member_id):
        # check if the book is borrowed by the member
        if self.member == member_id:
            # check if the book is overdue
            query = 'SELECT return_date FROM borrowed_books WHERE book_isbn = %s AND user_id = %s'
            params = (self.ISBN, member_id)
            return_date = self.db.fetch_query(query, params)
            if return_date:
                return_date = return_date[0][0]
                if datetime.now().strftime('%Y-%m-%d') > return_date:
                    days_overdue = (datetime.now() - datetime.strptime(return_date, '%Y-%m-%d')).days
                    fine = 2 * days_overdue
                    query = 'UPDATE users SET fines = fines + %s WHERE library_id = %s'
                    params = (fine, member_id)
                    self.db.execute_query(query, params)
                    print(f"You have been fined ${fine} for late return.")
            self.availability = True
            query = 'UPDATE books SET availability = %s, member = %s WHERE isbn = %s'
            params = (self.availability, self.member, self.ISBN)
            self.db.execute_query(query, params)
            # remove book from borrowed books table
            query = 'DELETE FROM borrowed_books WHERE book_isbn = %s AND user_id = %s'
            params = (self.ISBN, member_id)
            self.db.execute_query(query, params)
            self.member = None
            print(f"{self.title} has been returned.")
