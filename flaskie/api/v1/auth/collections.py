from ..models import User
from flaskie.database import db

    
def create_user(data):
    counter = 1
    db[counter] = data
    data.user_id = counter
    counter += 1

def get_user(user_id):
    return db.get(user_id)

def get_all_users(self):
    return db
        
def update_user(user_id, data):
    user = get_user(user_id)
    user.update_user(data)
    return user