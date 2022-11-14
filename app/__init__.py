from flask import Flask

from app import routes
from app.configs import database, env_configs, migration, jwt, cors



def create_app() -> Flask:
    app = Flask(__name__)

    cors.init_app(app)
    env_configs.init_app(app)
    database.init_app(app)
    migration.init_app(app)
    jwt.init_app(app)
    routes.init_app(app)

    return app
