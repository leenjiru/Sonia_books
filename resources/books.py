import sqlite3
from flask_jwt import jwt_required
from flask_restful import Resource, reqparse
from models.books import BookModel

books = []


class Book(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="Add a price to the book"
                        )

    @jwt_required()
    # jwt authenticates the user trying to access our resources
    def get(self, name):
        book = BookModel.find_by_name(name)
        if book:
            return book.json()
        return {'message': 'Book is not available'}, 404

    def post(self, name):
        book = BookModel.find_by_name(name)
        if book:
            return {'message': 'A book with name {} already exists'.format(name)}, 400

        request_data = Book.parser.parse_args()
        new_book = BookModel(name, request_data['price'])

        try:
            new_book.insert()
        except:
            return {'message': 'An error occurred while inserting.'}, 500

        return new_book.json(), 201

    def delete(self, name):
        if BookModel.find_by_name(name):
            connection = sqlite3.connect('data.db')
            cursor = connection.cursor()

            query = "DELETE FROM books WHERE name = ?"
            cursor.execute(query, (name,))

            connection.close()
            return {'message': 'Book deleted successfully'}
        else:
            return {'message': 'Book does not exist'}

    def put(self, name):
        request_data = Book.parser.parse_args()
        book = BookModel.find_by_name(name)
        new_book = BookModel(name, request_data['price'])

        if book:
            try:
                new_book.update()  # same as BookModel.insert(new_book) but since new book is an item model rather
                # than a dict it can be inserted this way
            except:
                return {'message': 'An error occurred while updating the book'}, 500
        else:
            try:
                new_book.insert()
            except:
                return {'message': 'An error occurred while updating the book'}, 500

        return new_book.json()


class Bookslist(Resource):
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM books"

        result = cursor.execute(query)

        for row in result:
            books.append({'name': row[0], 'price': row[1]})

        connection.close()
        return {'books': books}
