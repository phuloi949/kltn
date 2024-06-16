from database.auth_middleware import token_required

@token_required
def hello_world(current_user):
    """ Function which is triggered in flask app """
    _current_user = current_user["_id"]
    return _current_user