from database.auth_middleware import token_required

@token_required
def hello_world(current_user):
    """ Function which is triggered in flask app """
    return current_user