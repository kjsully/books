from flask import render_template, request, session, redirect

from flask_app import app
from ..models.author import Author
from ..models.book import Book



@app.route('/authors')
def index_author():
    authors = Author.get_all_authors()

    return render_template('authors.html', all_authors = authors)



@app.route('/authors/create', methods = ['POST'])
def create_author():
    print(request.form)
    Author.create(request.form)

    return redirect('/authors')



@app.route('/authors/<int:author_id>')
def show_author(author_id):
    return render_template(
    'author_show.html', 
    author = Author.get_one({'id': author_id}), all_books = Book.get_all_books()
    )



@app.route('/authors/<int:author_id>/add_book', methods = ['POST'])
def add_book(author_id):
    data = {
        'author_id': author_id,
        'book_id': request.form['book_id']
    }
    Author.add_book(data)

    return redirect (f"/authors/{author_id}")




@app.route('/')
def redirect_home():
    return redirect('/authors')