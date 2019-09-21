from typing import List

from flask import make_response

import app.config as cfg

data_type_map = {
    "id": int,
    "username": str,
    "firstname": str,
    "lastname": str,
    "mobile": str,
    "email": str,
    "empid": str,
    "organization": str,
    "status": str,
    "roles": List[str],
    "last_update": int
}


def validate_data_type(attrs: dict) -> list:
    keys = set(attrs.keys()) & cfg.all_attrs
    invalid_attrs = []
    for key in keys:
        if type(attrs[key]) != data_type_map[key]:
            invalid_attrs.append(key)

    return invalid_attrs


def get_message_from_exception(e: Exception):
    if str(e) == "UNIQUE constraint failed: USERS.USERNAME":
        return make_response("Username already exists", 409)
    elif str(e) == "FOREIGN KEY constraint failed":
        return make_response("Organization not found", 404)
    elif str(e) == "NOT NULL constraint failed: USERS.LASTNAME":
        return make_response("lastname cannot be empty", 409)
    elif str(e) == "NOT NULL constraint failed: USERS.USERNAME":
        return make_response("username cannot be empty", 409)
    return make_response(str(e), 400)
