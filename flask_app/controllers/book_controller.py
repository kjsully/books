from flask import render_template, request, session, redirect

from flask_app import app
from ..models.book import Book
from ..models.author import Author



@app.route('/books')
def index_book():
    books = Book.get_all_books()

    return render_template('books.html', all_books = books)



@app.route('/books/create', methods = ['POST'])
def create_book():
    print(request.form)
    Book.create(request.form)

    return redirect('/books')



@app.route('/books/<int:book_id>')
def show_book(book_id):
    return render_template(
        'books_show.html',
        book = Book.get_one({'id': book_id}),
        all_authors = Author.get_all_authors()
    )


@app.route('/books/<int:book_id>/add_book', methods = ['POST'])
def add_author(book_id):
    data = {
        'book_id': book_id, 
        'author_id': request.form['author_id']
    }
    Book.add_author(data)

    return redirect (f"/books/{book_id}")


@app.route('/')
def redirect_home2():
    return redirect('/authors')