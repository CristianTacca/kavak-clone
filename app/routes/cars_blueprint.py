from flask import Blueprint

from app.controllers.cars_controller import (
    get_cars,
    register_car,
    update_car,
    delete_car,
)

bp = Blueprint("cars", __name__, url_prefix="/cars")

bp.get("")(get_cars)
bp.post("/register/<user_id>")(register_car)
bp.patch("/<user_id>/<car_id>")(update_car)
bp.delete("/<user_id>/<car_id>")(delete_car)
