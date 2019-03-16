import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


def create_app(script=None):
    app = Flask(__name__)

    app_settings = os.getenv('APP_SETTINGS')
    app.config.from_object(app_settings)

    db.init_app(app)

    from project.api.users import users_namespace

    app.register_blueprint(users_namespace)

    @app.shell_context_processor
    def ctx():
        return {
            'app': app,
            'db': db,
        }

    return app
