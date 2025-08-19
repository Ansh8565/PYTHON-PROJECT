import json
import os

# Book Node
class Book:
    def __init__(self, book_id, title, author, status="Available"):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.status = status
        self.next = None 

# Libraryclass
class Library:
    def __init__(self):
        self.head = None  #listhead
        self.undo_stack = []  
        self.filename = "library_data.json"  # JSON file for persistence
        self.load_data()  # Load existing data on start

    # handling
    def save_data(self):
        """Save linked list to JSON file"""
        books = []
        current = self.head
        while current:
            books.append({
                "book_id": current.book_id,
                "title": current.title,
                "author": current.author,
                "status": current.status
            })
            current = current.next
        with open(self.filename, "w") as f:
            json.dump(books, f, indent=4)

    def load_data(self):
        """Load linked list from JSON file if exists"""
        if os.path.exists(self.filename):
            with open(self.filename, "r") as f:
                books = json.load(f)
                for b in reversed(books): #order
                    self.add_book(b["book_id"], b["title"], b["author"], b["status"], save=False)

    # core
    def add_book(self, book_id, title, author, status="Available", save=True):
        """Add a new book to the linked list"""
        new_book = Book(book_id, title, author, status)
        new_book.next = self.head
        self.head = new_book
        if save:
            self.save_data()
        print(f" Book '{title}' added successfully.")

    def display_books(self):
        """Display all books"""
        current = self.head
        if not current:
            print(" No books in the library.")
            return
        print("\n Library Inventory:")
        print("-" * 50)
        while current:
            print(f"[{current.book_id}] {current.title} by {current.author} - {current.status}")
            current = current.next
        print("-" * 50)

    def borrow_book(self, book_id):
        """Borrow a book by ID"""
        current = self.head
        while current:
            if current.book_id == book_id and current.status == "Available":
                current.status = "Borrowed"
                self.undo_stack.append(("borrow", current))
                self.save_data()
                print(f" You borrowed '{current.title}'.")
                return
            elif current.book_id == book_id and current.status == "Borrowed":
                print(" Book is already borrowed.")
                return
            current = current.next
        print("Book not found.")

    def return_book(self, book_id):
        """Return a borrowed book by ID"""
        current = self.head
        while current:
            if current.book_id == book_id and current.status == "Borrowed":
                current.status = "Available"
                self.undo_stack.append(("return", current))
                self.save_data()
                print(f"You returned '{current.title}'.")
                return
            elif current.book_id == book_id and current.status == "Available":
                print(" Book is not borrowed.")
                return
            current = current.next
        print(" Book not found.")

    def undo_action(self):
        """Undo last borrow/return action"""
        if not self.undo_stack:
            print("No actions to undo.")
            return
        action, book = self.undo_stack.pop()
        if action == "borrow":
            book.status = "Available"
            print(f" Undo: Borrowing of '{book.title}' has been reverted.")
        elif action == "return":
            book.status = "Borrowed"
            print(f" Undo: Returning of '{book.title}' has been reverted.")
        self.save_data()

    def search_books(self, keyword):
        """Search books by title or author"""
        current = self.head
        found = False
        keyword = keyword.lower()
        while current:
            if keyword in current.title.lower() or keyword in current.author.lower():
                print(f"[{current.book_id}] {current.title} by {current.author} - {current.status}")
                found = True
            current = current.next
        if not found:
            print(" No matching books found.")

#menu
def main():
    lib = Library()

    while True:
        print("\n====== E-Library Management System ======")
        print("1. Add Book")
        print("2. Display Books")
        print("3. Borrow Book")
        print("4. Return Book")
        print("5. Undo Last Action")
        print("6. Search Book")
        print("7. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            try:
                book_id = int(input("Enter Book ID: "))
                title = input("Enter Book Title: ")
                author = input("Enter Author Name: ")
                lib.add_book(book_id, title, author)
            except ValueError:
                print("Invalid input for Book ID. Must be a number.")

        elif choice == "2":
            lib.display_books()

        elif choice == "3":
            try:
                book_id = int(input("Enter Book ID to borrow: "))
                lib.borrow_book(book_id)
            except ValueError:
                print("Invalid input for Book ID.")

        elif choice == "4":
            try:
                book_id = int(input("Enter Book ID to return: "))
                lib.return_book(book_id)
            except ValueError:
                print("Invalid input for Book ID.")

        elif choice == "5":
            lib.undo_action()

        elif choice == "6":
            keyword = input("Enter title or author keyword: ")
            lib.search_books(keyword)

        elif choice == "7":
            print("Saving data & exiting...")
            lib.save_data()
            break

        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    main()
