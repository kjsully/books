from ..config.mysqlconnection import connectToMySQL

from ..models import book


class Author:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.books = []


    @classmethod
    def get_all_authors(cls):
        query = "SELECT * FROM authors;"

        results = connectToMySQL("books_schema").query_db(query)
        
        authors = []
        for row in results:
            authors.append(Author(row))

        print(authors)
        return authors


    @classmethod
    def create(cls, data):
        query = 'INSERT INTO authors (name) VALUES (%(name)s);'
        
        author_id = connectToMySQL('books_schema').query_db(query, data)
        
        print(author_id)
        return author_id


    @classmethod
    def get_one(cls, data):
        query = 'SELECT * FROM authors LEFT JOIN favorites ON authors.id = favorites.author_id LEFT JOIN books on books.id = favorites.book_id WHERE authors.id = %(id)s;'
        
        results = connectToMySQL('books_schema').query_db(query, data)

        author = Author(results[0])

        if results[0]['books.id'] != None:
            for row in results:
                row_data = {
                    'id': row['books.id'],
                    'title': row['title'],
                    'num_of_pages': row['num_of_pages'],
                    'created_at': row['books.created_at'],
                    'updated_at': row['books.updated_at'],
                }
                author.books.append(book.Book(row_data))

        print(results)
        return author


    @classmethod
    def add_book(cls, data):
        query = 'INSERT INTO favorites (author_id, book_id, created_at, updated_at) VALUES (%(author_id)s, %(book_id)s, NOW(), NOW());'
    
        return connectToMySQL('books_schema').query_db(query, data)
