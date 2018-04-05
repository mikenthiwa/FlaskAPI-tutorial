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
    users = {'mike.nthiwa': ('mike.nthiwa@gmail.com', 12345),
             'regina.nduku': ('reg.nduku@gmail.com', 6789)}

    def create_user(self, username, email, password):
        self.users[username] = (email, password)
        meta_user_data = self.users[username]
        email_data, password_data = meta_user_data
        return username, email_data, password_data

    def all_users(self):
        return self.users
