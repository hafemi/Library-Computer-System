import bcrypt
import json
import random
from fuzzywuzzy import process


class librarian:
    def add_book():
        title, author, release_date, description, id = get_book_information()
        book = {
            "title": title,
            "author": author,
            "releasedate": release_date,
            "description": description,
            "id": int(id), #some numbers can be a string
            "status": "rentable"
        }

        with open('books.json', 'r+') as file:
            file_content = json.load(file)
            file_content.append(book)
            file.seek(0)
            json.dump(file_content, file, indent=4)

    def see_rented_books():
        view_book_inventory('rented', 'There are no rented books', 'Times rented:')

    def see_book_stock():
        view_book_inventory('rentable', 'There are no rentable books', 'Copies:')

    def change_password():
        request_password()
        new_password = input("New Password: ").encode()
        hashed_password = bcrypt.hashpw(new_password, bcrypt.gensalt())

        with open("password.txt", "w") as file:
            file.write(str(hashed_password))


class visitor:
    def rent_book():
        manage_book_status('Book you want to rent: ', 'rentable', 'rented',
                           'Book is now being rented. Enjoy reading! :)',
                           'Book Title/ID cant be found or is not rentable')

    def return_book():
        manage_book_status('Book you want to return: ', 'rented', 'rentable',
                           'Book is rentable now.',
                           "Book Title/ID can't be found or is not rented")

    def search_for_book():
        desired_book = input('Search for Book/ID: ')
        if desired_book.isdigit():
            desired_book = int(desired_book) #turn string to int so we can search for id
        with open('books.json', 'r') as file:
            books = json.load(file)
            book_found = False #used to print message if no book is found

            for book in books:
                book_title, book_author, book_release, book_desc, book_id, book_status = get_book_data(book)
                if desired_book in (book_title, book_id):
                    book_found = True
                    print(' ') #placeholder
                    print(f'Title: {book_title} - Author: {book_author}')
                    print(f'Releasedate: {book_release}')
                    print(f'Description {book_desc}')
                    print(f'ID: {book_id} - Status: {book_status}')
            if not book_found:
                print('No Book found.')


valid_fuzzy_terms = {
    'roles': ['librarian', 'visitor'],
    'librarian': ['Add Book', 'See rented Books', 'See Book Stock', 'Change password', 'help'],
    'visitor': ['Rent Book', 'Return Book', 'See Book Stock', 'Search for Book', 'help']
}


actions_dict = {
    'librarian': {
        'add book': librarian.add_book,
        'see rented books': librarian.see_rented_books,
        'see book stock': librarian.see_book_stock,
        'change password': librarian.change_password
    },
    'visitor': {
        'rent book': visitor.rent_book,
        'see book stock': librarian.see_book_stock, #its librarian class because the function does the same
        'return book': visitor.return_book,
        'search for book': visitor.search_for_book
    }
}


def get_book_data(book):
    book_title = book.get('title')
    book_author = book.get('author')
    book_release = book.get('releasedate')
    book_desc = book.get('description')
    book_id = book.get('id')
    book_status = book.get('status')
    return book_title, book_author, book_release, book_desc, book_id, book_status


def change_status_if_existent(book, books, file, new_status, printmessage1):
    book['status'] = new_status #change status to rented/rentable
    file.seek(0)
    json.dump(books, file, indent=4)
    file.truncate()
    print(printmessage1) 


def manage_book_status(input_message, status, new_status, printmessage1, printmessage2): #used for 2 similar purposes
    while True:
        desired_book = input(input_message)
        if desired_book.isdigit():
            desired_book = int(desired_book) #turn string to int so we can search for id
               
        with open('books.json', 'r+') as file:
            books = json.load(file)
            for book in books:
                book_title = book.get('title')
                book_id = book.get('id')
                book_status = book.get('status')

                if desired_book in (book_title, book_id) and book_status == status:
                    change_status_if_existent(book, books, file, new_status, printmessage1)
                    break
            else:
                print(printmessage2)
            break


def make_books_list(books, status): #used for 2 similar purposes
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
                break
            if id == book_id: #generate new id if it already exists
                id = generate_random_id(id_list)
                break

        if id == '':
            id = generate_random_id(id_list)
        return id


def get_book_information():
    title = input('Whats the book title: ')
    author = input('Who is the author: ')
    release_date = input('When was the book published:  ')
    description = input('Description: ')
    id = int(input('Enter ID: '))
    id = confirm_inputs(id, title)
    return title, author, release_date, description, id


def get_input(role):
    while True:
        action = input('Action: ').lower()
        if action == 'help':
            print('Librarian - Add book, See rented books, See book stock, Change password')
            print('Visitor   - Rent book, Return book, See book stock, Search for book')

        elif action in actions_dict['librarian'] and role == 'librarian': #check if actions should be librarian's
            actions_dict['librarian'][action]()

        elif action in actions_dict['visitor'] and role == 'visitor': #check if actions should be visitor's
            actions_dict['visitor'][action]()

        else:
            fuzzy_list = process.extractOne(action, valid_fuzzy_terms[role]) #get the best matching action 
            print(f'There is no action named {action}, did you mean "{fuzzy_list[0]}"? Type "help" for more.')


def request_password():
    with open("password.txt", "r") as file:
        login_password = file.read().encode()[2:-1]  # turn string to byte and remove double quote mark
        while True:
            password = input("Password: ").encode()
            if bcrypt.hashpw(password, login_password) == login_password: #compare password with the login_password
                print("Password correct")
                break
            else:
                print("Invalid Passwort - Try again")
            print(' ')


while True:
    role = input("What role are you?: ").lower()
    fuzzy_list = process.extractOne(role, valid_fuzzy_terms["roles"]) #get the best matching role

    if fuzzy_list[1] == 100: #only run statement if input is 100% correct
        if role == "librarian":
            request_password()
            get_input(role)
        else:
            get_input(role)
    else:
        print(f'There is no role named {role}, did you mean "{fuzzy_list[0]}"?')
