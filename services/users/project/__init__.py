import os

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_debugtoolbar import DebugToolbarExtension
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy


bcrypt = Bcrypt()
db = SQLAlchemy()
migrate = Migrate()
toolbar = DebugToolbarExtension()


def create_app(script=None):
    app = Flask(__name__)

    CORS(app)

    app_settings = os.getenv('APP_SETTINGS')
    app.config.from_object(app_settings)

    db.init_app(app)
    toolbar.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)

    from project.api.users import users_blueprint
    from project.api.auth import auth_blueprint

    app.register_blueprint(users_blueprint)
    app.register_blueprint(auth_blueprint)

    @app.shell_context_processor
    def ctx():
        return {
            'app': app,
            'db': db,
        }

    return app
