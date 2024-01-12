import json

class Visitor:
    def __init__(self, lib_pc): #access functions inside LibraryComputer class
        self.lib_pc = lib_pc

    def rent_book(self):
        self.lib_pc.manage_book_status('rentable', 'rented', *self.lib_pc.custom_messages['rent book'])

    def return_book(self):
        self.lib_pc.manage_book_status('rented', 'rentable', *self.lib_pc.custom_messages['return book'])

    def search_for_book(self):
        desired_book = input('Search for Book/ID: ')
        if desired_book.isdigit():
            desired_book = int(desired_book) #turn string to int so we can search for id
        with open('books.json', 'r') as file:
            books = json.load(file)
            book_found = False #used to print message if no book is found

            for book in books:
                book_title, book_author, book_release, book_desc, book_id, book_status = self.lib_pc.get_book_data(book)
                if desired_book in (book_title, book_id):
                    book_found = True
                    print(' ') #placeholder
                    print(f'Title: {book_title} - Author: {book_author}')
                    print(f'Releasedate: {book_release}')
                    print(f'Description {book_desc}')
                    print(f'ID: {book_id} - Status: {book_status}')
            if not book_found:
                print('No Book found.')
