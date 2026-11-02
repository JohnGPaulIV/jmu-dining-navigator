"""Initialize the Flask application, database session, and appbuilder object."""

from flask import Flask
from flask_appbuilder import AppBuilder, IndexView
from flask_sqlalchemy import SQLAlchemy
from menu import setup_menu

class MyIndexView(IndexView):
    index_template = "index.jinja"

db = SQLAlchemy()
appbuilder = AppBuilder(indexview=MyIndexView)

def create_app():
    app = Flask(__name__)
    app.config.from_object("config")

    with app.app_context():
        db.init_app(app)
        appbuilder.init_app(app, db.session)  # type: ignore
        setup_menu(appbuilder)

    return app
