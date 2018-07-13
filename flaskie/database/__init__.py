from flask_jwt_extended import get_jwt_identity, jwt_required

db = {
    "paulla000": {
        'admin': True, 
        'email': 'paulla@gmail.com', 
        'name': 'Paulla Mboya', 
        'password_hash': '$2b$12$.X7XvBGCVVeRwPXrd3zQoean31S4RZQy6se4xAEJgngGda4fwveL2', 
        'registered_on': '2018-07-07T13:04:08.621684', 
        'username': 'paulla'
    }
}
blacklistdb = {}
requestsdb = {}


@jwt_required
def get_current_user():
    from flaskie.api.v1.auth.collections import store
    return store.get_by_field(key='username', value=get_jwt_identity())