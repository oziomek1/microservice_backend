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

    _initialize_extensions(app)
    _register_blueprints(app)

    # shell context for flask cli
    @app.shell_context_processor
    def ctx():
        return {
            'app': app,
            'db': db,
        }

    return app


def _initialize_extensions(app):
    db.init_app(app)
    toolbar.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)


def _register_blueprints(app):
    from project.api.routes.admin import admin_blueprint
    from project.api.routes.auth import auth_blueprint
    from project.api.routes.ping import ping_blueprint
    from project.api.routes.user import user_blueprint

    app.register_blueprint(admin_blueprint)
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(ping_blueprint)
    app.register_blueprint(user_blueprint)
