from database.set_db import db
from marshmallow import Schema, fields
from config import Config


class User(db.Model):
    __tablename__ = "user"
    __bind_key__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    password = db.Column(db.String)
    if Config.DEBUG:
        password_in_plain_view = db.Column(db.String)  # for debug only. Will be deleted if flask DEBUG == False
    role = db.Column(db.String)
    token_id = db.Column(db.Integer, db.ForeignKey('token.id'))

    token = db.relationship('Token', foreign_keys=[token_id])


class UserSchema(Schema):
    id = fields.Integer(dump_only=True)
    username = fields.String(unique=True)
    password = fields.String()
    if Config.DEBUG:
        password_in_plain_view = fields.String()  # for debug only. Will be deleted if flask DEBUG == False
    role = fields.String()
    token_id = fields.Integer()
