from flask_login import UserMixin


class Books:
    books = {1: ["Harry Potter", "J.K.Rowling"],
             2: ["The whistler", "John Grisham"]}

    def get_all_books(self):
        return self.books

    def get_a_book(self, book_id):
        int(book_id)
        return self.books.get(book_id, "{} does not exist".format(book_id))

    def borrow_book(self, book_id):
        int(book_id)
        return self.books.get(book_id)

    def add_book(self, book_id, book_title, author):
        self.books[book_id] = [book_title, author]
        return self.books

    def delete_book(self, book_id):
        del self.books[book_id]
        return self.books

    def update_book_info(self, book_id, book_title):
        self.books[book_id][0] = book_title
        return self.books


class Users(UserMixin):
    users = {"mike.nthiwa": ["mike.nthiwa@gmail.com", 123456789],
             "chris.mutua": ["c.mutua@gmail.com", 789456123]}

    def create_user(self, username, email, password):
        self.users[username] = [email, password]

    def all_users(self):
        return self.users

    def change_password(self, username, password):
        self.users[username][1] = password




