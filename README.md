# Library Computer System

## Description

A Simple representation of how a Library System could work with a CLI (Command Line Interface). Both librarians and visitors can do different tasks:

### Librarian functions
- Add a book with title, author, releasedate, description and id
- See a list of all rented books and how many of the same name are rented
- Changing password which is required in the beginning at choosing the role
- Seeing all the books that are not rented

### Visitor functions
- Renting a book by the title/id and getting a book recommendation
- Return a book by title/id
- See all rentable books
- Search for a book by title/id


There are also additional functions that check/do different things, such as:
- generate new ID if the input was empty/not available id
- check if the same title exists and if so change the id according to that
- "did you mean .." errors with fuzzy search
- password is being saved in a hashed version (irreversible string)

## Setup

This Project only contains the code/files for it. To use it you already need an IDE (Integrated Development Environment), for example, Visual Studio Code (python extension needed), Pycharm etc.
In case you have any of these, just download the files/copy the code and put it inside the folder where your project is located (all 3 are needed).

After running the code, you are going to get instructions on what you can do. In order to choose the librarian role, you have to enter a password, which is "test1".

## Credits
To learn different things, I have read through these websites, but of course they are not the only ones:
- Fuzzy search: https://www.datacamp.com/tutorial/fuzzy-string-python or https://www.geeksforgeeks.org/fuzzywuzzy-python-library/
- Hashing Password: https://www.geeksforgeeks.org/how-to-hash-passwords-in-python/
