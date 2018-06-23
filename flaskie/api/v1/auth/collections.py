from ..models import User, MainModel
from flaskie.database import db
from .serializers import Pagination


def create_user(data):
    name = data['name']
    username = data['username']
    email = data['email']
    password = data['password_hash']
    role = data['role']
    user = User(name, username, email, password, role)
    counter = 0
    db.append(user.toJSON())
    for item in db:
        item['user_id'] = counter = counter + 1
    print(db)
    response = {
        'status': 'success',
        'message': 'Successfully registered',
        'new_user': user.toJSON()
    }
    return response, 201


def get_user(user_id):
    return db.get(user_id)

def get_all_users():
    return db
        
def update_user(user_id, data):
    user = get_user(user_id)
    user.update_user(data)
    return user