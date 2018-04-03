from flask import Flask, jsonify, request
from data import Books, Users
app = Flask(__name__)


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
            password = req_data[u_name][e_mail]

    user.create_user(username, email, password)

    return jsonify(user.all_users())


if __name__ == '__main__':
    app.run(debug=True)
