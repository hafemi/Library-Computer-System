import bcrypt
import json
import random
import visitor
import librarian
import os
import re
from fuzzywuzzy import process


class LibraryComputer:
    def __init__(self): #get access to the classes
        self.librarian = librarian.Librarian(self)
        self.visitor = visitor.Visitor(self)
        self.actions_dict = {
            'librarian': {
                'add book': self.librarian.add_book,
                'see rented books': self.librarian.see_rented_books,
                'see book stock': self.librarian.see_book_stock,
                'change password': self.librarian.change_password
            },
            'visitor': {
                'rent book': self.visitor.rent_book,
                'see book stock': self.librarian.see_book_stock, #its librarian class because the function does the same
                'return book': self.visitor.return_book,
                'search for book': self.visitor.search_for_book
            }
        }

    valid_fuzzy_terms = {
        'roles': ['librarian', 'visitor'],
        'librarian': ['Add Book', 'See rented Books', 'See Book Stock', 'Change password', 'help'],
        'visitor': ['Rent Book', 'Return Book', 'See Book Stock', 'Search for Book', 'help']
    }

    custom_messages = { #some functions take the same arguments but different print messages
        'see rented books': ['There are no rented books', 'Times rented:'],
        'see book stock': ['There are no rentable books', 'Copies:'],
        'return book': ['Book you want to return: ', 'Book is rentable now.', 'Book Title/ID cant be found or is not rented'],
        'rent book':  ['Book you want to rent: ', 'Book is now being rented. Enjoy reading! :)', 'Book Title/iD cant be found or is not rentable']
    }

    def get_book_data(self, book):
        book_title = book.get('title')
        book_author = book.get('author')
        book_release = book.get('releasedate')
        book_desc = book.get('description')
        book_id = book.get('id')
        book_status = book.get('status')
        return book_title, book_author, book_release, book_desc, book_id, book_status

    def change_status_if_existent(self, book, books, file, new_status, printmessage1):
        book['status'] = new_status #change status to rented/rentable
        file.seek(0)
        json.dump(books, file, indent=4)
        file.truncate()
        print(printmessage1) 

    def manage_book_status(self, status, new_status, input_message, printmessage1, printmessage2): #used for 2 similar purposes
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
                        self.change_status_if_existent(book, books, file, new_status, printmessage1)
                        break
                else:
                    print(printmessage2)
                break

    def make_books_list(self, books, status): #used for 2 similar purposes
        books_list = []
        for book in books:
            book_title = book.get('title')
            book_status = book.get('status')
            if book_status == status:
                books_list.append(book_title)
        return books_list

    def filter_books_list(self, books_list, books):
        filtered_books = books_list.copy()
        for book in books:
            book_title = book.get('title')
            while filtered_books.count(book_title) > 1: #remove multiple existing title until 1
                filtered_books.remove(book_title)
        return filtered_books

    def view_book_inventory(self, status, printmessage1, printmessage2): #used for 2 different purposes
        with open('books.json', 'r') as file:
            books = json.load(file)

            books_list = self.make_books_list(books, status)
            filtered_books = self.filter_books_list(books_list, books)

            if books_list == []:
                print(printmessage1)
            else:
                for book in filtered_books:
                    print("Title:", book)
                    print(printmessage2, books_list.count(book))
                    print(' ')

    def generate_random_id(self, id_list):
        while True:
            random_id = random.randint(1, 99999)
            if not random_id in id_list:
                return random_id

    def confirm_inputs(self, id, title):
        with open('books.json', 'r') as file:
            books = json.load(file)

            id_list = []
            for book in books:
                book_id = book.get('id')
                book_title = book.get('title')
                id_list.append(book_id) # id's to avoid for random generating
                if id:
                    id = int(id)
                    if title == book_title: # overwrite id if double existing title
                        id = book_id
                        break
                    if id == book_id: #generate new id if it already exists
                        id = self.generate_random_id(id_list)
                        break

            if id == '': 
                id = self.generate_random_id(id_list)
            return id

    def get_book_information(self):
        while True:
            title = input('Whats the book title: ')
            author = input('Who is the author: ')
            release_date = input('When was the book published: ')
            description = input('Description: ')
            id = input('Enter ID: ')
            id = self.confirm_inputs(id, title)

            if not all([title, author, release_date, description]):
                print('Fill out every detail.')
                continue
            if not re.match(r'\d{1,2}\.\d{1,2}\.\d{4}', release_date):
                print('Invalid Date format, use dd.mm.yy (1.1.2000)')
                continue
            
            return title, author, release_date, description, id

    def get_input(self, role):
        while True:
            action = input('Action: ').lower()
            if action == 'help':
                print('Librarian - Add book, See rented books, See book stock, Change password')
                print('Visitor   - Rent book, Return book, See book stock, Search for book')

            elif action in self.actions_dict['librarian'] and role == 'librarian': #check if actions should be librarian's
                self.actions_dict['librarian'][action]()

            elif action in self.actions_dict['visitor'] and role == 'visitor': #check if actions should be visitor's
                self.actions_dict['visitor'][action]()

            else:
                fuzzy_list = process.extractOne(action, self.valid_fuzzy_terms[role]) #get the best matching action 
                print(f'There is no action named {action}, did you mean "{fuzzy_list[0]}"? Type "help" for more.')

    def request_password(self):
        with open("password.txt", "r") as file:
            login_password = file.read().encode()  # turn string to byt
            while True:
                password = input("Password: ").encode()
                if bcrypt.hashpw(password, login_password) == login_password: #compare password with the login_password
                    print("Password correct")
                    break
                else:
                    print("Invalid Passwort - Try again")
                print(' ')

    def main(self):
        while True:
            role = input("What role are you?: ").lower()
            fuzzy_list = process.extractOne(role, self.valid_fuzzy_terms["roles"]) #get the best matching role

            if fuzzy_list[1] == 100: #run statement if input is 100% correct
                if role == "librarian":
                    script_directory = os.path.dirname(os.path.abspath(__file__))
                    file_path = os.path.join(script_directory, 'password.txt')

                    if not os.path.exists(file_path): #create password when theres no password.txt file
                        password = input('There is no Password, enter a new one: ').encode()
                        hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
                        with open(file_path, 'w') as f: f.write(hashed_password.decode())

                    else:    
                        self.request_password()

                self.get_input(role)
            else:
                print(f'There is no role named {role}, did you mean "{fuzzy_list[0]}"?')

computer = LibraryComputer()
computer.main()