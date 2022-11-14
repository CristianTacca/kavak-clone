from http import HTTPStatus
from flask import jsonify, request
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import IntegrityError, DataError

from app.configs.database import db
from app.models.user_model import User
from app.exceptions.user_exceptions import NameFormatError, EmailFormatError
from app.exceptions.request_data_exceptions import MissingAttributeError
from app.services.general_services import (
    incoming_values,
    check_keys,
    check_keys_type,
)

session: Session = db.session


def create_user():
    data = request.get_json()

    empty_values = incoming_values(data)

    if empty_values:
        return empty_values, HTTPStatus.BAD_REQUEST

    valid_keys = ["name", "email", "password"]
    try:
        new_data = check_keys(data, valid_keys)
    except MissingAttributeError as m:
        return m.response, HTTPStatus.BAD_REQUEST

    keys_types = {"name": str, "email": str, "password": str}
    try:
        check_keys_type(new_data, keys_types)
    except AttributeError as e:
        return e.response, HTTPStatus.BAD_REQUEST

    try:
        new_user = User(**new_data)
        session.add(new_user)
        session.commit()
    except NameFormatError as e:
        return e.response, e.status_code
    except EmailFormatError:
        return {
            "error": f'Email format not acceptable: {new_data["email"]}, try ex.: your_mail@your_provider.com'
        }, HTTPStatus.BAD_REQUEST
    except IntegrityError as e:
        session.rollback()
        error = str(e)
        if "Key (email)" in error:
            return {"error": "Email already exists."}, HTTPStatus.CONFLICT
    except DataError as e:
        session.rollback()
        error = str(e)

        return {
            "error": "Name has to be less than 120 letters. If your name is greater than that, try abbreviate it."
        }, HTTPStatus.BAD_REQUEST

    return jsonify(new_user), HTTPStatus.CREATED
