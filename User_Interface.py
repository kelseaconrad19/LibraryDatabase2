
from Database import Database
from Author import Author
from book import Book
from mysql.connector import Error
from member import Member
import json
import re

db = Database('127.0.0.1', 'root', 'jeweller-zipper-reck2', 'new_library')


# DONE
def main_menu():
    print(f"Welcome to the Library Management System!")
    while True:
        menu_choice = input(
            "Main Menu:\n1. Book Operations\n2. Member Operations\n3. Author Operations\n4. Genre Operations\n6. Quit\n")
        if menu_choice == "1":
            book_operations()
        elif menu_choice == '2':
            member_operations()
        elif menu_choice == '3':
            catalog_operations()
        elif menu_choice == '4':
            author_operations()
        elif menu_choice == '5':
            genre_operations()
        elif menu_choice == '6':
            break
        else:
            print("Invalid choice. Please try again.")


# DONE
def author_operations():
    print("Author Operations")
    while True:
        author_choice = input(
            "1. Add a new author\n2. View author details\n3. Display all authors\n4. Quit\n")
        if author_choice == '1':  # Add a new author - DONE
            name = input("Enter the author's name: ")
            bio = input("Enter the author's biography: ")
            author = Author(db, name, bio)
            author.save_author()
            print("Author added successfully.")
        elif author_choice == '2':  # View author details - DONE
            name = input("Enter the author's name: ")
            author = Author.get_by_name(name, db)
            if author:
                print(f"Name: {author.name}\nBiography: {author.biography}")
        elif author_choice == '3':  # Display all authors - DONE
            query = "SELECT * FROM authors"
            authors = db.fetch_query(query)
            if authors:
                for author in authors:
                    print(f"Name: {author[1]}\nBiography: {author[2]}\n")
            else:
                print("No authors found.")
        elif author_choice == '4':  # Quit
            break
        else:
            print("Invalid choice. Please try again.")


def book_operations(database=db):
    print("Book Operations:")
    while True:
        book_menu_choice = input("1. Add a new book\n2. Search for a Book\n3. Borrow a book\n4. Return a book\n5. Display all Books\n6. Quit\n")
        if book_menu_choice == "1":  # Add a new book
            title = input("Enter the title of the book: ")
            author_id = input("Enter the author id: ")
            isbn = input("Enter the ISBN of the book: ")
            genre_id = input("Enter the genre id: ")
            member = input("Enter the member id: ")
            book = Book(title, author_id, isbn, genre_id, member, database)
            try:
                book.save_book()
                print("Book added successfully.")
            except Error as e:
                print(f"Error: {e}")
        elif book_menu_choice == "2":  # Search for a book
            title = input("Enter the title of the book you want to search for: ")
            book = Book.get_by_title(title, database)
            if book.availability:
                print(f"{book.title} is available.")
            else:
                print(f"{book.title} is not available.")
        elif book_menu_choice == "3":  # Borrow a book
            # Change the availability of the book to False and assign the book to the member; update the database.
            title = input("Enter the title of the book you want to borrow: ")
            book = Book.get_by_title(title, database)
            if book:
                member_id = input("Enter your member id: ")
                book.check_out_book(member_id)
            else:
                print(f"{title} not found.")
        elif book_menu_choice == "4":  # Return a book
            title = input("Enter the title of the book you want to return: ")
            book = Book.get_by_title(title, database)
            print(book.title, book.member)
            if book:
                member_id = input("Enter your member id: ")
                book.return_book(member_id)
            else:
                print(f"{title} not found.")
        elif book_menu_choice == "5":  # Display all Books
            Book.display_all_books(database)

        elif book_menu_choice == "6":  # Quit
            break
        else:
            print("Invalid choice. Please try again.")


def member_operations(database=db):
    print("Member Operations:")
    while True:
        member_menu_choice = input("1. Add a new member\n2. View member details\n3. Display all members\n4. Quit\n")
        if member_menu_choice == "1":  # Add a new member
            name = input("Enter the member's name: ")
            library_card_id = input("Enter the member's library card id: ")
            fines = input("Enter the member's fines: ")
            member = Member(name, library_card_id, fines, db)
            member.save_member()
            print("Member added successfully.")
        elif member_menu_choice == "2":  # View member details
            library_card_id = input("Enter the member's library card id: ")
            member = Member.display_member_info(library_card_id, db)
            if member:
                print(member)
            else:
                print("Member not found.")
        elif member_menu_choice == "3":  # Display all members
            Member.display_all_members(db)
        elif member_menu_choice == "4":  # Quit
            break
        else:
            print("Invalid choice. Please try again.")


def catalog_operations():
    pass


def genre_operations():
    pass
