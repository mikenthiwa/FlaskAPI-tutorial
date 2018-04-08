from flask_login import UserMixin


class Books:
    books = {}

    def get_all_books(self):
        return self.books

    def get_a_book(self, book_id):
        int(book_id)
        return self.books.get(book_id, "{} does not exist".format(book_id))

    def add_book(self, book_id, book_title):
        self.books[book_id] = {"Title": book_title}
        return self.books

    def delete_book(self, book_id):
        del self.books[book_id]
        return self.books

    def update_book_info(self, book_id, book_title):
        self.books[book_id]["Title"] = book_title
        return self.books


class Users(UserMixin):
    users = {}

    def create_user(self, username, email, password):
        self.users[username] = [email, password]

    def all_users(self):
        return self.users

    def change_password(self, username, password):
        self.users[username][1] = password




