from web_base._endpoint_handler import EndpointHandler
from web_base.colored_print import print_colored
from web_base.text_art import art_fl_apiserverstart
"""
    This is an abstraction for Flask server
"""
class FlaskAppWrapper(object):

    def __init__(self, app, **configs):
        self.app = app
        self.configs(**configs)
        print_colored(art_fl_apiserverstart, "green")
        

    def configs(self, **configs):
        for config, value in configs:
            self.app.config[config.upper()] = value

    def add_endpoint(self, endpoint=None, endpoint_name=None, handler=None, methods=['GET'], *args, **kwargs):
        self.app.add_url_rule(endpoint, endpoint_name, EndpointHandler(handler), methods=methods, *args, **kwargs)

    def run(self, **kwargs):
        self.app.run(**kwargs)
        print_colored(art_fl_apiserverstart, "green")
