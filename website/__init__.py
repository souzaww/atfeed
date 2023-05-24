from flask import Flask
from os import path
from flask_login import LoginManager
from .database import create_db, Queries

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .database import Queries,User, Note, Feed
    
    with app.app_context():
        create_db()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    #função para carregar o usuário logado
    @login_manager.user_loader
    def load_user(id):
        return Queries.get_user_by_id(id)
    
    return app