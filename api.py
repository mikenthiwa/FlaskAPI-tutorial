from flask import Flask, jsonify, request
from data import Books, Users
from flask_jwt_extended import (JWTManager, jwt_required, create_access_token, get_jwt_identity)

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'super-secret'
jwt = JWTManager(app)
book = Books()
user = Users()
users = user.all_users()
books = book.get_all_books()


@app.route('/', methods=['GET'])
def index():
    return jsonify({"message": "it works"})


@app.route('/api/auth/register', methods=['POST'])
def new_user():
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


@app.route('/api/auth/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({"msg": "Missing json in request"}), 400
    username = request.json.get('username', None)
    password = request.json.get('password', None)

    if not username and not password:
        return jsonify({"msg": 'username and password are empty'})
    elif not username:
        return jsonify({"msg": 'username is empty'})
    elif not password:
        return jsonify({"msg": 'password is empty'})
    else:
        if username not in users:
            return jsonify({'msg': "Invalid user"})
        elif password != users[username][1]:
            return jsonify({"msg": 'wrong password'})

    access_token = create_access_token(identity=username)

    return jsonify(access_token=access_token), 200


@app.route('/api/v1/books', methods=['GET'])
def all_books():
    return jsonify(book.get_all_books())


@app.route('/api/v1/users/books/<int:book_id>', methods=['GET'])
@jwt_required
def borrow(book_id):
    current_user = get_jwt_identity()
    print(type(book_id))
    if current_user in users:
        if book_id in books:
            print('available')
    return jsonify(logged_in_as=current_user), 200


@app.route('/api/v1/books/<int:book_id>', methods=['GET'])
def specific_book(book_id):
    return jsonify(book.get_a_book(book_id))


@app.route('/api/v1/books/<int:book_id>', methods=['PUT'])
def modify_book_info(book_id):
    req_data = request.get_json()
    book_info = ""

    for values in req_data.values():
        for value in values.values():
            book_info = value

    book.update_book_info(book_id, book_info)
    return jsonify(book.get_all_books())


@app.route('/api/books/<book_id>', methods=['DELETE'])
def remove_a_book(book_id):

    try:
        book.delete_book(book_id)
    except KeyError:
        print(book_id.isalpha())
    return jsonify(book.get_all_books())


@app.route('/api/v1/books', methods=['POST'])
def add_new_book():

    req_data = request.get_json()
    book_id = ""
    author = ""
    title = ""

    for key in req_data:
        book_id = key
        for key_val in req_data[key]:
            title = key_val
            author = req_data[key][key_val]

    book.add_book(int(book_id), title, author)
    return "You have added\nBook_Id: {}\nTitle: {}\nAuthor: {}".format(book_id, title, author)


@app.route('/api/auth/reset-password', methods=['POST'])
def reset_password():
    req_data = request.get_json()
    user_data = user.all_users()
    e_mail = ""
    password = ""
    username = ""
    for email in req_data:
        e_mail = email
        password = req_data[e_mail]

    for u_name in user_data:
        username = u_name
        if user_data[username][0] == e_mail:
            user.change_password(username, password)

    return 'Username : {}\nNew password : {}'.format(username, password)


if __name__ == '__main__':
    app.run(debug=True)
