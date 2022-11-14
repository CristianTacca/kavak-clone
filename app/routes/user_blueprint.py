from flask import Blueprint

from app.controllers.user_controller import create_user

bp = Blueprint("users", __name__, url_prefix="/users")

bp.post("/register")(create_user)
