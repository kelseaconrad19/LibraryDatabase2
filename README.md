# Library Management System

This is a simple library management system built in Python. It allows users to manage books, members, and genres in a library.

## Features

- Add, delete, and search for books.
- Borrow and return books.
- Add and view member details.
- Add and view genre details.

## Prerequisites

- Python 3.x
- MySQL

## Setup

1. Clone the repository.
2. Navidage to the project directory.
3. Install the required packages.
4. Update the database configuration in `main.py` with your MySQL credentials.

## Usage

Run the `main.py` script to start the program:

Once the program is running, you will be presented with a main menu with the following options:

1. Book Operations
2. Member Operations
3. Genre Operations
4. Quit

### Book Operations

In the Book Operations menu, you can:

1. Add a new book: You will be asked to enter the book's title, author, genre, and ISBN.
2. Delete a book: Enter the title of the book you want to delete.
3. Search for a book: Enter the title of the book you want to search for.
4. Borrow a book: Enter the title of the book you want to borrow and your member id.
5. Return a book: Enter the title of the book you want to return and your member id.
6. Display all books: This will print a list of all books in the library.
7. Quit: Return to the main menu.

### Member Operations

In the Member Operations menu, you can:

1. Add a new member: You will be asked to enter the member's name, library card id, and fines.
2. View member details: Enter the member's library card id to view their details.
3. Display all members: This will print a list of all members in the library.
4. Quit: Return to the main menu.

### Genre Operations

In the Genre Operations menu, you can:

1. Add a new genre: You will be asked to enter the genre's name, description, and category.
2. View genre details: Enter the genre's name to view its details.
3. Display all genres: This will print a list of all genres in the library.
4. Quit: Return to the main menu.
