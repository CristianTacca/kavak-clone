from flask import Flask

from app.routes.cars_blueprint import bp as bp_cars
from app.routes.user_blueprint import bp as bp_user
from app.routes.login_blueprint import bp as bp_login


def init_app(app: Flask):
    app.register_blueprint(bp_cars)
    app.register_blueprint(bp_user)
    app.register_blueprint(bp_login)
