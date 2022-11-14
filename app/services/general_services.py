from difflib import SequenceMatcher

from app.configs.database import db
from app.exceptions.invalid_id_exception import InvalidIdError
from app.exceptions.request_data_exceptions import (
    MissingAttributeError,
    AttributeTypeError,
    IncorrectKeys,
)


def remove_unnecessary_keys(data: dict, necessary_keys: list):
    new_data = data.copy()
    not_used_keys = necessary_keys.copy()

    for key in data.keys():
        if key in necessary_keys:
            not_used_keys.remove(key)
        else:
            new_data.pop(key)

    return (new_data, not_used_keys)


def incoming_values(data):
    values_data = [value for value in data.values()]

    if "" in values_data:
        return {"error": "Incoming value is empty."}


def check_keys(data: dict, mandatory_keys: list):
    new_data, missing_keys = remove_unnecessary_keys(data, mandatory_keys)

    if missing_keys:
        raise MissingAttributeError(missing_keys)

    return new_data


def check_keys_type(data: dict, keys_type: dict):
    for key, value in data.items():
        if type(value) is not keys_type[key]:
            raise AttributeTypeError(data, keys_type)


def check_id_validation(id: str, model: db.Model = None):
    if len(id) != 36:
        raise InvalidIdError(
            message={"error": f"The id {id} is not valid"}, status_code=400
        )
    search = model.query.filter_by(id=id).first()
    if not search:
        raise InvalidIdError(
            message={"error": f"The id {id} is not in database."}
        )


def is_string_similar(s1: str, s2: str, threshold: float = 0.8):
    return SequenceMatcher(a=s1, b=s2).ratio() > threshold


def similar_keys(data, valid_keys, not_used_keys):
    invalid_keys = [key for key in data.keys() if key not in valid_keys]

    error_keys = []
    for key in invalid_keys:
        for not_used in not_used_keys:
            similar = is_string_similar(key, not_used)
            if similar is True:
                error_keys.append(key)

    if error_keys:
        raise IncorrectKeys(error_keys)
