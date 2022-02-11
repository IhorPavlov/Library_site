# from Library.storages.orm_storage import ORMStorage
# # from client_handler import ClientHandler
# from Library.library import Library
# from socket import socket


from flask import Flask, render_template, request

from Library.library import Library
from Library.storages.orm_storage import ORMStorage

CURRENT_USER_ID = 1

import os
from dotenv import load_dotenv
load_dotenv('.env')


app = Flask(__name__,
            template_folder='../site/templates',
            static_folder='../site/static')

app.config['DEBUG'] = True
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')


storage = ORMStorage(
    db_user=os.environ.get('DB_USER'),
    db_password=os.environ.get('DB_PASSWORD'),
    db_name=os.environ.get('DB_NAME'),
    db_address=os.environ.get('DB_ADDRESS'),
    db_port=os.environ.get('DB_PORT')
)

lib = Library(storage)
if not lib.get_all_books():
    lib.load_books_from_txt_file('books.txt', sep='$!$')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/books', methods=['GET'])
def api_get_all_books():
    return render_template('books.html', books=lib.get_all_books())


@app.route('/add_book', methods=['GET', 'POST'])
def api_add_book():
    if request.method == 'POST':
        title_book = request.form.get('title')
        author_book = request.form.get('author')
        year_book = request.form.get('year')

        if not (title_book and author_book and year_book):
            return render_template('add_book.html', message='Введены некорректные данные')
        if not year_book.isnumeric():
            return render_template('add_book.html', message='Введен некорректный год издания')

        ret_code, ret_msg = lib.add_book(title_book, author_book, int(year_book))
        return render_template('add_book.html', message=ret_msg)

    return render_template('add_book.html')

    # # WTForm
    # from add_book_form import AddBookForm
    # add_book_form = AddBookForm()
    #
    # if request.method == 'POST':
    #     if add_book_form.validate_on_submit():
    #         print(add_book_form.title.data)
    #         print(add_book_form.author.data)
    #         print(add_book_form.year.data)
    #     else:
    #         print('Error')
    #
    # return render_template('add_book.html', form=add_book_form)


@app.route('/delete_book', methods=['GET', 'POST'])
def api_delete_book():
    if request.method == 'POST':
        id_books = [int(i) for i in request.form.keys() if i.isnumeric()]

        if len(id_books):
            ret_msg = lib.remove_books(id_books)
            return render_template('delete_book.html',
                                   books=sorted(lib.get_all_books(), key=lambda book: book.id),
                                   message=ret_msg)

    return render_template('delete_book.html', books=sorted(lib.get_all_books(), key=lambda book: book.id))


@app.route('/take_book', methods=['GET', 'POST'])
def api_take_book():
    if request.method == 'POST':
        id_books = [int(i) for i in request.form.keys() if i.isnumeric()]

        if len(id_books):
            message = lib.give_books(id_books, CURRENT_USER_ID)
            return render_template('take_book.html',
                                   books=sorted(lib.get_available_books(), key=lambda book: book.id),
                                   message=message)

    return render_template('take_book.html', books=sorted(lib.get_available_books(), key=lambda book: book.id))


@app.route('/return_book', methods=['GET', 'POST'])
def api_return_book():
    if request.method == 'POST':
        id_books = [int(i) for i in request.form.keys() if i.isnumeric()]

        if len(id_books):
            message = lib.return_books(id_books, CURRENT_USER_ID)
            return render_template('return_book.html',
                                   books=sorted(lib.get_all_book_from_reader(CURRENT_USER_ID),
                                                key=lambda book: book.id),
                                   message=message)

    return render_template('return_book.html',
                           books=sorted(lib.get_all_book_from_reader(CURRENT_USER_ID), key=lambda book: book.id))


@app.route('/registration', methods=['GET', 'POST'])
def api_registration():
    if request.method == 'POST':
        pass

    return render_template('registration.html')


@app.route('/login', methods=['GET', 'POST'])
def api_login():
    if request.method == 'POST':
        pass

    return render_template('login.html')


if __name__ == '__main__':
    app.run()

# def start_server(ip: str, port: int, lib: Library):
#     with socket() as sock:
#         sock.bind((ip, port))
#         sock.listen(5)
#
#         while True:
#             conn, _ = sock.accept()
#             print(f'connected: {_}')
#             client = ClientHandler(conn, lib)
#             client.start()

# if __name__ == '__main__':
#
#     ip = '127.0.0.1'
#     port = 12347
#
#     storage = ORMStorage()
#
#     lib = Library(storage)
#
#     if not lib.load_books():
#         lib.load_books_from_txt_file('./Library/init_data/books.txt', sep='$!$')
#
#     if not lib.load_readers():
#         lib.load_readers_from_txt_file('./Library/init_data/readers.txt')
#
#     start_server(ip, port, lib)