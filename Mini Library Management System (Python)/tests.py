# Test data structures and functions directly
from Operations import *
books = {}
members = []
member_counter = 1
GENRES = ("Fiction", "Non-Fiction", "Sci-Fi", "Mystery", "Biography", "Fantasy", "History")

def add_book(isbn, title, author, genre, total_copies=1):
    global books
    if isbn in books:
        return False
    if genre not in GENRES:
        return False
    books[isbn] = {
        'title': title,
        'author': author,
        'genre': genre,
        'total_copies': total_copies,
        'available_copies': total_copies
    }
    return True

def add_member(name, email):
    global members, member_counter
    for member in members:
        if member['email'] == email:
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
    return member_id

def borrow_book(member_id, isbn):
    global books, members
    member = next((m for m in members if m['member_id'] == member_id), None)
    if not member:
        return False
    if isbn not in books:
        return False
    if len(member['borrowed_books']) >= 3:
        return False
    if books[isbn]['available_copies'] <= 0:
        return False
    if isbn in member['borrowed_books']:
        return False
    member['borrowed_books'].append(isbn)
    books[isbn]['available_copies'] -= 1
    return True

def return_book(member_id, isbn):
    global books, members
    member = next((m for m in members if m['member_id'] == member_id), None)
    if not member:
        return False
    if isbn not in member['borrowed_books']:
        return False
    member['borrowed_books'].remove(isbn)
    books[isbn]['available_copies'] += 1
    return True

def delete_book(isbn):
    global books
    if isbn not in books:
        return False
    if books[isbn]['available_copies'] < books[isbn]['total_copies']:
        return False
    del books[isbn]
    return True

def delete_member(member_id):
    global members
    member = next((m for m in members if m['member_id'] == member_id), None)
    if not member:
        return False
    if member['borrowed_books']:
        return False
    members.remove(member)
    return True

# Tests
def test_add_book():
    global books
    books.clear()
    assert add_book("1234567890", "Test Book", "Test Author", "Fiction") == True
    assert "1234567890" in books
    assert add_book("1234567890", "Another Book", "Another Author", "Sci-Fi") == False
    assert add_book("0987654321", "Invalid Book", "Some Author", "Invalid Genre") == False
    print("✓ test_add_book passed")

def test_add_member():
    global members, member_counter
    members.clear()
    member_counter = 1
    member_id = add_member("John Doe", "john@example.com")
    assert member_id == 1
    assert len(members) == 1
    add_member("Jane Doe", "john@example.com")
    assert len(members) == 1
    print("✓ test_add_member passed")

def test_borrow_return_books():
    global books, members, member_counter
    books.clear()
    members.clear()
    member_counter = 1
    add_book("1111111111", "Book 1", "Author 1", "Fiction", 2)
    add_member("Test Member", "test@example.com")
    assert borrow_book(1, "1111111111") == True
    assert books["1111111111"]['available_copies'] == 1
    assert "1111111111" in members[0]['borrowed_books']
    assert return_book(1, "1111111111") == True
    assert books["1111111111"]['available_copies'] == 2
    assert "1111111111" not in members[0]['borrowed_books']
    print("✓ test_borrow_return_books passed")

def test_borrow_limits():
    global books, members, member_counter
    books.clear()
    members.clear()
    member_counter = 1
    add_member("Test Member", "test@example.com")
    add_book("1111111111", "Book 1", "Author 1", "Fiction")
    add_book("2222222222", "Book 2", "Author 2", "Sci-Fi")
    add_book("3333333333", "Book 3", "Author 3", "Mystery")
    add_book("4444444444", "Book 4", "Author 4", "Biography")
    assert borrow_book(1, "1111111111") == True
    assert borrow_book(1, "2222222222") == True
    assert borrow_book(1, "3333333333") == True
    assert borrow_book(1, "4444444444") == False
    print("✓ test_borrow_limits passed")

def test_delete_with_dependencies():
    global books, members, member_counter
    books.clear()
    members.clear()
    member_counter = 1
    add_book("1111111111", "Book 1", "Author 1", "Fiction")
    add_member("Test Member", "test@example.com")
    borrow_book(1, "1111111111")
    assert delete_book("1111111111") == False
    assert delete_member(1) == False
    print("✓ test_delete_with_dependencies passed")

def run_all_tests():
    print("Running Library Management System Tests...\n")
    test_add_book()
    test_add_member()
    test_borrow_return_books()
    test_borrow_limits()
    test_delete_with_dependencies()
    print("\n🎉 All tests passed!")

if __name__ == "__main__":
    run_all_tests()