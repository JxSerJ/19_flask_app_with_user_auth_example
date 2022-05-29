from typing import Any

from marshmallow import ValidationError

from database.set_db import db


def validator(method: str, request_data: Any, Obj: object, Obj_schema: object) -> None:
    # validating data structure

    obj_keys = set(Obj_schema.fields.keys())
    obj_keys.remove('id')
    if "token_id" in obj_keys:
        obj_keys.remove('token_id')
    if 'password_in_plain_view' in obj_keys:
        obj_keys.remove('password_in_plain_view')

    data_keys = request_data.keys()
    if 'id' in data_keys:
        data_keys = set(data_keys.remove('id'))
    else:
        data_keys = set(data_keys)
    if data_keys != obj_keys:
        messages = {}
        diff1 = obj_keys.difference(data_keys)
        diff2 = data_keys.difference(obj_keys)
        if method in ["PUT", "POST"]:
            for diff_entry in diff1:
                messages[diff_entry] = "Missing field"
        for diff_entry in diff2:
            messages[diff_entry] = "Unknown field"
        if len(messages) > 0:
            error_text_entry = {"PUT": [" full", "required"],
                                "POST": [" full", "required"],
                                "PATCH": ["", "available"]}
            msg = {"error": "Validation Error. Invalid structure found in request body data. "
                            "{} request must contain only{} dataset with valid keys for successful "
                            "processing. {} data keys enumerated in corresponding field"
                            .format(method, error_text_entry[method][0],
                            error_text_entry[method][1].title()),
                   f"{error_text_entry[method][1]}_keys": list(obj_keys),
                   "incorrect_data": messages}

            raise ValidationError(message=msg)

    if method == 'POST':
        # validating if database already contains data

        if Obj.__name__ == "Movie":
            query = db.session.query(Obj).filter(Obj.title == request_data['title'],
                                                 Obj.year == request_data['year'],
                                                 Obj.director_id == request_data['director_id']).first()
            db.session.close()
        elif Obj.__name__ == "User":
            query = db.session.query(Obj).filter(Obj.username == request_data['username']).first()
            db.session.close()
        else:
            query = db.session.query(Obj).filter(Obj.name == request_data['name']).first()
            db.session.close()

        query_data = Obj_schema.dump(query)
        if len(query_data) > 0:
            msg = f"{Obj.__name__} already in database. {Obj.__name__} ID: {query.id}"
            raise ValidationError(message=msg)
