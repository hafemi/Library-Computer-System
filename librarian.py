import json
import bcrypt

class Librarian:
    def __init__(self, lib_pc): #access functions inside LibraryComputer class
        self.lib_pc = lib_pc

    def add_book(self):
        title, author, release_date, description, id = self.lib_pc.get_book_information()
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

    def see_rented_books(self):
        self.lib_pc.view_book_inventory('rented', *self.lib_pc.custom_messages['see rented books'])

    def see_book_stock(self):
        self.lib_pc.view_book_inventory('rentable', *self.lib_pc.custom_messages['see book stock'])

    def change_password(self): #turn string to byte and write it to the file as string
        self.lib_pc.request_password()
        new_password = input("New Password: ").encode()
        hashed_password = bcrypt.hashpw(new_password, bcrypt.gensalt())

        with open("password.txt", "w") as file:
            file.write(str(hashed_password.decode()))