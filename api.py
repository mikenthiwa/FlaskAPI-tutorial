from flask import Flask, jsonify, request
from data import Books, Users
from flask_login import LoginManager, current_user

app = Flask(__name__)

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return Users.get_id(user_id)


@app.route('/api/auth/login', methods=['POST'])
def login():
    books = Books()
    user = Users()
    if current_user.is_authenticated:
        return jsonify(books.get_all_books())
    user_cred = request.get_json()
    all_users = user.all_users()
    username_password_db = {}

    for u_name in all_users:
        username_password_db[u_name] = all_users[u_name][1]

    for u_name in user_cred:
        if u_name in username_password_db:
            if user_cred[u_name] == username_password_db[u_name]:
                return jsonify(books.get_all_books())
            else:
                return 'Wrong password'
        else:
            return 'Invalid username. Register ?'


@app.route('/', methods=['GET'])
def index():
    return jsonify({"message": "it works"})


@app.route('/api/books', methods=['GET'])
def all_books():
    books = Books()
    return jsonify(books.get_all_books())


@app.route('/api/books/<int:book_id>', methods=['GET'])
def specific_book(book_id):
    book = Books()
    return jsonify(book.get_a_book(book_id))


@app.route('/api/books/<int:book_id>', methods=['PUT'])
def modify_book_info(book_id):
    book = Books()
    req_data = request.get_json()
    book_info = ""

    for values in req_data.values():
        for value in values.values():
            book_info = value

    book.update_book_info(book_id, book_info)
    return jsonify(book.get_all_books())


@app.route('/api/books/<book_id>', methods=['DELETE'])
def remove_a_book(book_id):
    book = Books()
    try:
        book.delete_book(book_id)
    except KeyError:
        print(book_id.isalpha())
    return jsonify(book.get_all_books())


@app.route('/api/books', methods=['GET', 'POST'])
def add_new_book():
    new_book = Books()

    if request.method == 'POST':
        req_data = request.get_json()
        keys = ""
        values = ""

        for key in req_data.keys():
            keys = key

        for data in req_data.values():
            for value in data.values():
                values = value

        new_book.add_book(int(keys), values)
    return jsonify(new_book.get_all_books())


@app.route('/api/auth/register', methods=['POST'])
def new_user():
    user = Users()
    req_data = request.get_json()
    username = ""
    email = ""
    password = ""
    for u_name in req_data:
        username = u_name
        for e_mail in req_data[u_name]:
            email = e_mail
            if len(str(req_data[u_name][e_mail])) < 8:
                return 'password length is short'
            password = req_data[u_name][e_mail]

    user.create_user(username, email, password)
    return "Username : {}\nPassword : {}\n\nPlease Log In".format(username, password)


@app.route('/api/auth/reset-password', methods=['POST'])
def reset_password():
    users = Users()

    req_data = request.get_json()
    user_data = users.all_users()
    e_mail = ""
    password = ""
    username = ""
    for email in req_data:
        e_mail = email
        password = req_data[e_mail]

    for u_name in user_data:
        username = u_name
        if user_data[username][0] == e_mail:
            users.change_password(username, password)

    return 'Username : {}\nNew password : {}'.format(username, password)


if __name__ == '__main__':
    app.run(debug=True)
