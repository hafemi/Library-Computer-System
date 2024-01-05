import bcrypt
import json
import random
from fuzzywuzzy import process

valid_fuzzy_terms = {
    'roles': ['librarian', 'visitor'],
    'librarian_actions': ['Add Book', 'See rented Books', 'See Book Stock', 'Change password', 'help']
}


class librarian:
    def get_input():
        while True:
            action = input('Action: ').lower()
            match action:
                case 'add book':
                    librarian.add_book()
                case 'see rented books':
                    librarian.see_rented_books()
                case 'see book stock':
                    librarian.see_book_stock()
                case 'change password':
                    librarian.change_password()
                case 'help':
                    print('All actions:')
                    print('1. Add book 2. See rented books 3. See book stock 4. Change password')
                case _:
                    fuzzy_list = process.extractOne(action, valid_fuzzy_terms['librarian_actions'])
                    print(f'There is no action named {action}, did you mean "{fuzzy_list[0]}"? Type "help" for more.')

    def add_book():
        title, author, release_date, description, id = get_book_information()
        book = {
            "title": title,
            "author": author,
            "releasedate": release_date,
            "description": description,
            "id": int(id),
            "status": "rentable"
        }

        with open('books.json', 'r+') as file:
            file_content = json.load(file)
            file_content.append(book)
            file.seek(0)
            json.dump(file_content, file, indent=4)

    def see_rented_books():
        view_book_inventory('There are no rented books', 'rented', 'Times rented:')

    def see_book_stock():
        view_book_inventory('There are no rentable books', 'rentable', 'Copies:')

    def change_password():
        request_password()
        new_password = input("New Password: ").encode()
        hashed_password = bcrypt.hashpw(new_password, bcrypt.gensalt())

        with open("password.txt", "w") as file:
            file.write(str(hashed_password))


def make_books_list(books, status): #used for 2 different purposes
    books_list = []
    for book in books:
        book_title = book.get('title')
        book_status = book.get('status')
        if book_status == status:
            books_list.append(book_title)
    return books_list


def filter_books_list(books_list, books):
    filtered_books = books_list.copy()
    for book in books:
        book_title = book.get('title')
        while filtered_books.count(book_title) > 1: #remove multiple existing title until 1
            filtered_books.remove(book_title)
    return filtered_books


def view_book_inventory(status, printmessage1, printmessage2): #used for 2 different purposes
    with open('books.json', 'r') as file:
        books = json.load(file)

        books_list = make_books_list(books, status)
        filtered_books = filter_books_list(books_list, books)

        if books_list == []:
            print(printmessage1)
        else:
            for book in filtered_books:
                print("Title:", book)
                print(printmessage2, books_list.count(book))
                print(' ')
    

def generate_random_id(id_list):
    while True:
        random_id = random.randint(1, 99999)
        if not random_id in id_list:
            return random_id


def confirm_inputs(id, title):
    with open('books.json', 'r') as file:
        books = json.load(file)

        id_list = []
        for book in books:
            book_id = book.get('id')
            book_title = book.get('title')
            id_list.append(book_id) # id's to avoid for random generating
            if title == book_title: # overwrite id if double existing title
                id = book_id

        if id == '':
            id = generate_random_id(id_list)
        return id


def get_book_information():
    title = input('Whats the book title: ')
    author = input('Who is the author: ')
    release_date = input('When was the book published:  ')
    description = input('Description: ')
    id = input('Enter ID: ')
    id = confirm_inputs(id, title)
    return title, author, release_date, description, id


def request_password():
    with open("password.txt", "r") as file:
        login_password = file.read().encode()[2:-1]  # turn string to byte and remove double quote mark
        while True:
            password = input("Password: ").encode()
            if bcrypt.hashpw(password, login_password) == login_password:
                print("Password correct")
                break
            else:
                print("Invalid Passwort - Try again")
            print(' ')


while True:
    role = input("What role are you?: ").lower()
    fuzzy_list = process.extractOne(role, valid_fuzzy_terms["roles"])

    if fuzzy_list[1] == 100:
        if role == "librarian":
            request_password()
            librarian.get_input()
        else:
            print("...")  # placeholder for now
    else:
        print(f'There is no role named {role}, did you mean "{fuzzy_list[0]}"?')
