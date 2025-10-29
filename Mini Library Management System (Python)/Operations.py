# operations.py

books = {}
members = []
genres = ("Fiction", "Non-Fiction", "Sci-Fi", "Romance", "History")

# Add a book
def add_book(isbn, title, author, genre, total):
    if isbn in books:
        return "Book already exists."
    if genre not in genres:
        return "Invalid genre."
    books[isbn] = {"title": title, "author": author, "genre": genre, "total": total, "available": total}
    return "Book added successfully."

# Add a member
def add_member(member_id, name, email):
    for m in members:
        if m["member_id"] == member_id:
            return "Member ID already exists."
    members.append({"member_id": member_id, "name": name, "email": email, "borrowed_books": []})
    return "Member added successfully."

# Search books
def search_books(keyword):
    result = []
    for isbn, details in books.items():
        if keyword.lower() in details["title"].lower() or keyword.lower() in details["author"].lower():
            result.append((isbn, details))
    return result

# Update book
def update_book(isbn, title=None, author=None, total=None):
    if isbn not in books:
        return "Book not found."
    if title: books[isbn]["title"] = title
    if author: books[isbn]["author"] = author
    if total: 
        diff = total - books[isbn]["total"]
        books[isbn]["total"] = total
        books[isbn]["available"] += diff
    return "Book updated successfully."

# Delete book
def delete_book(isbn):
    if isbn not in books:
        return "Book not found."
    for m in members:
        if isbn in m["borrowed_books"]:
            return "Cannot delete. Book borrowed."
    del books[isbn]
    return "Book deleted."

# Borrow book
def borrow_book(member_id, isbn):
    for m in members:
        if m["member_id"] == member_id:
            if isbn not in books:
                return "Book not found."
            if books[isbn]["available"] == 0:
                return "No copies left."
            if len(m["borrowed_books"]) >= 3:
                return "Borrow limit reached."
            m["borrowed_books"].append(isbn)
            books[isbn]["available"] -= 1
            return "Book borrowed."
    return "Member not found."

# Return book
def return_book(member_id, isbn):
    for m in members:
        if m["member_id"] == member_id:
            if isbn in m["borrowed_books"]:
                m["borrowed_books"].remove(isbn)
                books[isbn]["available"] += 1
                return "Book returned."
            return "Book not borrowed by this member."
    return "Member not found."
