from typing import Any

from marshmallow import ValidationError

from database.set_db import db


def validator(method: str, request_data: Any, Obj: object, Obj_schema: object) -> None:
    # validating data structure

    movie_keys = set(Obj_schema.fields.keys())
    movie_keys.remove('id')
    data_keys = request_data.keys()
    if 'id' in data_keys:
        data_keys = set(data_keys.remove('id'))
    else:
        data_keys = set(data_keys)
    if data_keys != movie_keys:
        messages = {}
        diff1 = movie_keys.difference(data_keys)
        diff2 = data_keys.difference(movie_keys)
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
                   f"{error_text_entry[method][1]}_keys": list(movie_keys),
                   "incorrect_data": messages}

            raise ValidationError(message=msg)

    if method == 'POST':
        # validating if database already contains data

        if Obj.__name__ == "Movie":
            query = db.session.query(Obj).filter(Obj.title == request_data['title'],
                                                 Obj.year == request_data['year'],
                                                 Obj.director_id == request_data['director_id']).first()
            db.session.close()
        else:
            query = db.session.query(Obj).filter(Obj.name == request_data['name']).first()
            db.session.close()

        query_data = Obj_schema.dump(query)
        if len(query_data) > 0:
            msg = f"Data already in database. Data ID: {query.id}"
            raise ValidationError(message=msg)
