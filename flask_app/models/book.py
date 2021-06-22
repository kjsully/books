from ..config.mysqlconnection import connectToMySQL

from ..models import author


class Book:
    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.num_of_pages = data['num_of_pages']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.authors = []

    
    @classmethod
    def get_all_books(cls):
        query = "SELECT * FROM books;"

        results = connectToMySQL("books_schema").query_db(query)
        books = []

        for row in results:
            books.append(Book(row))

        print(books)
        return books



    @classmethod
    def create(cls, data):
        query = 'INSERT INTO books (title, num_of_pages) VALUES (%(title)s, %(num_of_pages)s);'

        book_id = connectToMySQL('books_schema').query_db(query, data)

        print(book_id)
        return book_id



    @classmethod
    def get_one(cls, data):
        query = 'SELECT * FROM books LEFT JOIN favorites ON books.id = favorites.book_id LEFT JOIN authors on authors.id = favorites.author_id WHERE books.id = %(id)s;'
        
        results = connectToMySQL('books_schema').query_db(query, data)

        book = Book(results[0])

        if results[0]['authors.id'] != None:
            for row in results:
                row_data = {
                    'id': row['authors.id'],
                    'name': row['name'],
                    'created_at': row['authors.created_at'],
                    'updated_at': row['authors.updated_at']
                }
                book.authors.append(author.Author(row_data))

        
        return book


    @classmethod
    def add_author(cls, data):
        query = 'INSERT INTO favorites (author_id, book_id, created_at, updated_at) VALUES (%(author_id)s, %(book_ids)s, NOW(), NOW());'

        return connectToMySQL('books_schema').query_db(query, data)