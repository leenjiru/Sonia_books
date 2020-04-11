# for an in memory database this code can be used

from flask_jwt import jwt_required
from flask_restful import Resource, reqparse


class Book(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="Add a price to the book"
                        )

    @jwt_required()  # jwt authenticates the user trying to access our resources
    def get(self, name):
        """
        #the lambda function simplifies the access
         for book in books:
             if book['name'] == name:
                 return book
        #here a user tries to access a book from the server, if book is found it will be returned else an error
        since the user may have made a typo error
        """
        book = next(filter(lambda x: x['name'] == name, books), None)
        return {'book': book}, 200 if book else 404

    def post(self, name):
        """
        # a user uploads or posts a books, if already exists, will be notified so
        in post we have to pass data from the server to compare with what we're getting
        """
        if next(filter(lambda x: x['name'] == name, books), None):
            return {'Message': "The book with name '{}' already exists".format(name)}, 400

        request_data = Book.parser.parse_args()

        book = {'name': name, 'price': request_data['price']}
        books.append(book)
        return book, 201

    def delete(self, name):
        global books
        books = list(filter(lambda x: x['name'] != name, books))
        return {'Message': 'Book has been deleted'}

    def put(self, name):
        """
        #This is another way of doing it but is repetitive in every function
         parser = reqparse.RequestParser()
         parser.add_argument('price',
                             type=float,
                             help="Book cannot be passed without a price tag"
                             )
         request_data = request.get_json()
        """
        request_data = Book.parser.parse_args()

        book = next(filter(lambda x: x['name'] == name, books), None)
        if book is None:
            book = {'name': name, 'price': request_data['price']}
            books.append(book)
        else:
            book.update(request_data)
        return book


class Bookslist(Resource):
    def get(self):
        return {'books': books}
