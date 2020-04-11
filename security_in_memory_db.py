# this applies when using an in memory db

from models.users import UserModel
from werkzeug.security import safe_str_cmp

# users = [
#     {
#         'id': 1,
#         'username': 'Nick',
#         'Password': 'password'
#     }
# ]
users = [
    UserModel(1, 'Nicky', 'password1')
]

username_mapping = {u.username: u for u in users}
user_id_mapping = {u.id: u for u in users}


# user_id_mapping = {
#     1: {
#         'id': 1,
#         'username': 'Nick',
#         'Password': 'password'
#     }
# }


def authenticate(username, password):
    user = username_mapping.get(username, None)
    if user and safe_str_cmp(user.password, password):
        return user


def identity(payload):
    user_id = payload['identity']
    return user_id_mapping.get(user_id, None)
