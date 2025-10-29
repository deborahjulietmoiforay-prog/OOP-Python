# Copy the essential functions and data structures
from Operations import *

books = {}
members = []
member_counter = 1
GENRES = ("Fiction", "Non-Fiction", "Sci-Fi", "Mystery", "Biography", "Fantasy", "History")


def add_book(isbn, title, author, genre, total_copies=1):
    global books
    if isbn in books:
        print(f"Error: Book with ISBN {isbn} already exists.")
        return False
    if genre not in GENRES:
        print(f"Error: Invalid genre. Must be one of: {GENRES}")
        return False
    books[isbn] = {
        'title': title,
        'author': author,
        'genre': genre,
        'total_copies': total_copies,
        'available_copies': total_copies
    }
    print(f"Book '{title}' added successfully.")
    return True


def add_member(name, email):
    global members, member_counter
    for member in members:
        if member['email'] == email:
            print(f"Error: Member with email {email} already exists.")
            return None
    member_id = member_counter
    member_counter += 1
    new_member = {
        'member_id': member_id,
        'name': name,
        'email': email,
        'borrowed_books': []
    }
    members.append(new_member)
    print(f"Member '{name}' added successfully with ID: {member_id}")
    return member_id


def search_book(search_term):
    results = []
    search_term = search_term.lower()
    for isbn, book in books.items():
        if (search_term in book['title'].lower() or
                search_term in book['author'].lower()):
            results.append({
                'isbn': isbn,
                **book
            })
    return results


def borrow_book(member_id, isbn):
    global books, members
    member = next((m for m in members if m['member_id'] == member_id), None)
    if not member:
        print(f"Error: Member with ID {member_id} not found.")
        return False
    if isbn not in books:
        print(f"Error: Book with ISBN {isbn} not found.")
        return False
    if len(member['borrowed_books']) >= 3:
        print("Error: Member cannot borrow more than 3 books.")
        return False
    if books[isbn]['available_copies'] <= 0:
        print("Error: No copies of this book are available.")
        return False
    if isbn in member['borrowed_books']:
        print("Error: Member already has this book borrowed.")
        return False
    member['borrowed_books'].append(isbn)
    books[isbn]['available_copies'] -= 1
    print(f"Book '{books[isbn]['title']}' borrowed successfully by {member['name']}.")
    return True


def return_book(member_id, isbn):
    global books, members
    member = next((m for m in members if m['member_id'] == member_id), None)
    if not member:
        print(f"Error: Member with ID {member_id} not found.")
        return False
    if isbn not in member['borrowed_books']:
        print("Error: Member does not have this book borrowed.")
        return False
    member['borrowed_books'].remove(isbn)
    books[isbn]['available_copies'] += 1
    print(f"Book '{books[isbn]['title']}' returned successfully by {member['name']}.")
    return True


def delete_book(isbn):
    global books
    if isbn not in books:
        print(f"Error: Book with ISBN {isbn} not found.")
        return False
    if books[isbn]['available_copies'] < books[isbn]['total_copies']:
        print("Error: Cannot delete book - some copies are currently borrowed.")
        return False
    book_title = books[isbn]['title']
    del books[isbn]
    print(f"Book '{book_title}' deleted successfully.")
    return True


def delete_member(member_id):
    global members
    member = next((m for m in members if m['member_id'] == member_id), None)
    if not member:
        print(f"Error: Member with ID {member_id} not found.")
        return False
    if member['borrowed_books']:
        print("Error: Cannot delete member - they have borrowed books.")
        return False
    members.remove(member)
    print(f"Member '{member['name']}' deleted successfully.")
    return True


def display_books():
    print("\n--- Library Books ---")
    for isbn, book in books.items():
        print(f"ISBN: {isbn}, Title: {book['title']}, Author: {book['author']}, "
              f"Genre: {book['genre']}, Available: {book['available_copies']}/{book['total_copies']}")


def display_members():
    print("\n--- Library Members ---")
    for member in members:
        print(f"ID: {member['member_id']}, Name: {member['name']}, "
              f"Email: {member['email']}, Borrowed Books: {len(member['borrowed_books'])}")


def run_demo():
    """Demonstrate all system functionalities"""
    print(" Library Management System Demo")
    print("=" * 40)

    # Clear any existing data
    books.clear()
    members.clear()
    global member_counter
    member_counter = 1

    # 1. Add Books
    print("\n1. ADDING BOOKS")
    print("-" * 20)
    add_book("9780451524935", "1984", "George Orwell", "Fiction", 3)
    add_book("9780141439518", "Pride and Prejudice", "Jane Austen", "Fiction", 2)
    add_book("9780765311788", "Mistborn", "Brandon Sanderson", "Fantasy", 4)
    add_book("9780307277671", "The Da Vinci Code", "Dan Brown", "Mystery", 3)
    add_book("9781401309573", "The Last Lecture", "Randy Pausch", "Non-Fiction", 1)

    # 2. Add Members
    print("\n2. ADDING MEMBERS")
    print("-" * 20)
    add_member("Alice Johnson", "alice@email.com")
    add_member("Bob Smith", "bob@email.com")
    add_member("Carol Davis", "carol@email.com")

    # 3. Display Current State
    print("\n3. CURRENT LIBRARY STATE")
    print("-" * 20)
    display_books()
    display_members()

    # 4. Search Books
    print("\n4. SEARCHING BOOKS")
    print("-" * 20)
    print("Searching for 'George':")
    results = search_book("George")
    for book in results:
        print(f"  - {book['title']} by {book['author']}")

    print("\nSearching for 'Code':")
    results = search_book("Code")
    for book in results:
        print(f"  - {book['title']} by {book['author']}")

    # 5. Borrow Books
    print("\n5. BORROWING BOOKS")
    print("-" * 20)
    borrow_book(1, "9780451524935")
    borrow_book(1, "9780141439518")
    borrow_book(2, "9780765311788")

    # 6. Try to borrow when limit reached
    print("\n6. TESTING BORROWING LIMITS")
    print("-" * 20)
    borrow_book(1, "9780307277671")
    borrow_book(1, "9781401309573")

    # 7. Return Books
    print("\n7. RETURNING BOOKS")
    print("-" * 20)
    return_book(1, "9780451524935")

    # 8. Display Updated State
    print("\n8. UPDATED LIBRARY STATE")
    print("-" * 20)
    display_books()
    display_members()

    # 9. Delete Operations
    print("\n9. DELETION OPERATIONS")
    print("-" * 20)
    delete_member(1)
    return_book(1, "9780141439518")
    return_book(2, "9780765311788")
    delete_member(1)
    delete_book("9780451524935")

    # 10. Final State
    print("\n10. FINAL LIBRARY STATE")
    print("-" * 20)
    display_books()
    display_members()

    print("\n🎉 Demo completed successfully!")


if __name__ == "__main__":
    run_demo()