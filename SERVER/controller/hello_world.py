from database.auth_middleware import token_required

@token_required
def hello_world(current_user):
    """ Function which is triggered in flask app """
    _current_user = current_user["_id"]
    _current_username = current_user["username"]
    return f"You are now {_current_username} with _id as {_current_user}"