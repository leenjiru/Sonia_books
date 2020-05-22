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
        if BookModel.find_by_name(name):
            return {'message': 'A book with name {} is available'.format(name)}, 400
        request_data = Book.parser.parse_args()
        book = BookModel(name, request_data['price'])
        try:
            book.save_to_db()
        except:
            return {'message': 'Error occurred while saving to db'}, 500
        return book.json(), 201

    def delete(self, name):
        book = Book.find_by_name(name)
        if book:
            book.delete_from_db()
        return {'message': 'book deleted'}

    def put(self, name):
        request_data = Book.parser.parse_args()
        book = BookModel.find_by_name(name)

        if book is None:
            book = BookModel(name, request_data['price'])
        else:
            book.price = request_data['price']

        book.save_to_db()

        return book.json()


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
