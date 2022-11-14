from http import HTTPStatus

from flask import request, jsonify
from sqlalchemy.orm import Query
from sqlalchemy.orm.session import Session
from flask_jwt_extended import jwt_required
from sqlalchemy.exc import IntegrityError, DataError


from app.configs.database import db
from app.models.user_model import User
from app.models.cars_model import Cars
from app.exceptions.user_exceptions import NotLoggedUserError
from app.exceptions.invalid_id_exception import InvalidIdError
from app.exceptions.request_data_exceptions import (
    MissingAttributeError,
    IncorrectKeys,
    AttributeTypeError,
)
from app.services.general_services import (
    incoming_values,
    check_id_validation,
    remove_unnecessary_keys,
    similar_keys,
    check_keys,
    check_keys_type,
)

session: Session = db.session


def get_cars():
    cars: Query = session.query(Cars).select_from(Cars).all()

    return jsonify(cars)


@jwt_required()
def register_car(user_id: str):
    try:
        check_id_validation(user_id, User)
    except NotLoggedUserError as e:
        return e.response, e.status_code
    except InvalidIdError as e:
        return e.response, e.status_code

    data = request.get_json()

    empty_values = incoming_values(data)
    if empty_values:
        return empty_values, HTTPStatus.BAD_REQUEST

    valid_keys = ["marca", "modelo", "valor", "ano", "km", "cidade", "estado", "foto"]
    try:
        new_data = check_keys(data, valid_keys)
    except MissingAttributeError as m:
        return m.response, HTTPStatus.BAD_REQUEST

    keys_types = {"marca": str, "modelo": str, "valor": int, "ano": int, "km": int, "cidade": str, "estado": str, "foto": str}
    try:
        check_keys_type(new_data, keys_types)
    except AttributeError as e:
        return e.response, HTTPStatus.BAD_REQUEST

    try:
        new_car = Cars(**new_data)
        session.add(new_car)
        session.commit()
    except IntegrityError as e:
        session.rollback()
        error = str(e)

        return {"error": error}
    except DataError as e:
        session.rollback()
        error = str(e)

        return {"error": error}

    return jsonify(new_car), HTTPStatus.CREATED


@jwt_required()
def update_car(user_id: str, car_id: int):
    try:
        check_id_validation(user_id, User)
    except NotLoggedUserError as e:
        return e.response, e.status_code

    car: Query = (
        session.query(Cars).select_from(Cars).filter(Cars.id == car_id).first()
    )

    if not car:
        return {
            "error": "There is no car in database with that id."
        }, HTTPStatus.BAD_REQUEST

    data = request.get_json()

    empty_values = incoming_values(data)
    if empty_values:
        return empty_values, HTTPStatus.BAD_REQUEST

    valid_keys = ["marca", "modelo", "valor", "ano", "km", "foto", "cidade", "estado", "vendido", "promocao"]
    new_data, not_used_keys = remove_unnecessary_keys(data, valid_keys)

    try:
        similar_keys(data, valid_keys, not_used_keys)

        if new_data == {}:
            return {"error": "No data to update"}, HTTPStatus.BAD_REQUEST

        type_keys = {
            "marca": str,
            "modelo": str,
            "valor": int,
            "ano": int,
            "km": int,
            "cidade": str,
            "estado": str,
            "foto": str,
            "vendido": bool,
            "promocao": bool,
        }
        check_keys_type(new_data, type_keys)

        for key, value in new_data.items():
            setattr(car, key, value)

        session.commit()
    except IncorrectKeys as e:
        return e.response, e.status_code
    except AttributeTypeError as e:
        return e.response, e.status_code
    except IntegrityError as e:
        session.rollback()
        error = str(e)

        return {"error": error}

    return {"msg": "your car has been updated.", "car": car}, HTTPStatus.OK


@jwt_required()
def delete_car(user_id: str, car_id: str):

    try:
        check_id_validation(user_id, User)
    except NotLoggedUserError as e:
        return e.response, e.status_code

    car: Query = (
        session.query(Cars).select_from(Cars).filter(Cars.id == car_id).first()
    )

    session.delete(car)
    session.commit()

    return "", HTTPStatus.NO_CONTENT
