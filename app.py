from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from security import authenticate, identity

from resources.books import Bookslist, Book
from resources.users import RegisterUsers

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////mnt/C:/Users/LEE/PycharmProjects/Sonia_Restful/data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'secret'
api = Api(app)


jwt = JWT(app, authenticate, identity)  # authentication

api.add_resource(Book, '/book/<string:name>')
api.add_resource(Bookslist, '/books')
api.add_resource(RegisterUsers, '/register')

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(debug=True)
