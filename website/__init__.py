from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'asdf'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://ale@mysqlserverale:Test12345!@mysqlserverale.mysql.database.azure.com/test'

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    return app

