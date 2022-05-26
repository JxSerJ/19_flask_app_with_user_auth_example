from database.set_db import db
from marshmallow import Schema, fields


class Director(db.Model):
    __tablename__ = "director"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)


class DirectorSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(unique=True)
