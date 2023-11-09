from flask import Flask
from flask_login import LoginManager
from Infrastructure.mongodb_repository import MongoDBRepository


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "topsecretkey"
    
    from Routes.home import homeviews
    from Routes.auth import authviews
    app.register_blueprint(homeviews, url_prefix='/')
    app.register_blueprint(authviews, url_prefix='/')

    mongodb_repository = MongoDBRepository()
    app.mongodb_repository = mongodb_repository
    
    login_manager = LoginManager()
    login_manager.login_view = 'authviews.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(username):
        user_data = mongodb_repository.find_user(username)
        if user_data:
            return user_data
        return None
    
    return app