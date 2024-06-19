from flask import request, make_response
"""
    This is abstraction for Endpoint
"""
class EndpointHandler(object):

    def __init__(self, action):
        self.action = action 

    def __call__(self, *args, **kwargs):
        response = self.action(*args, **request.view_args)
        return make_response(response)