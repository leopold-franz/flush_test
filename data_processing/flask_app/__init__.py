from flask import Flask


def create_app():
    '''
    Create an flask_app by initializing components.
    '''
    app = Flask(__name__)

    return app
