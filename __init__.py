from flask import Flask

def create_app():
    app = Flask(__name__)

    print(__name__)
    
    return app