from flask import Flask
from Infrastructure.mongodb_repository import MongoDBRepository


def create_app():
    app = Flask(__name__)

    from Routes.home import homeviews

    app.register_blueprint(homeviews, url_prefix='/')
    
    mongodb_repository = MongoDBRepository()

    app.mongodb_repository = mongodb_repository

    return app