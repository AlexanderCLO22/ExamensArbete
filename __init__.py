from flask import Flask

def create_app():
    app = Flask(__name__)

    from Routes.home import homeviews

    app.register_blueprint(homeviews, url_prefix='/')
    
    return app