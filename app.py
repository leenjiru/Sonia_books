from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from security import authenticate, identity

from resources.books import Bookslist, Book
from resources.users import RegisterUsers

app = Flask(__name__)
app.secret_key = 'secret'
api = Api(app)

jwt = JWT(app, authenticate, identity)  # authentication
books = []

api.add_resource(Book, '/book/<string:name>')
api.add_resource(Bookslist, '/books')
api.add_resource(RegisterUsers, '/register')

if __name__ == '__main__':
    app.run(debug=True)
