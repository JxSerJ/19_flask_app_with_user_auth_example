from database.set_db import db
from marshmallow import Schema, fields


class Token(db.Model):
    __tablename__ = "token"
    __bind_key__ = "tokens"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    access_token = db.Column(db.String)
    refresh_token = db.Column(db.String)

    user = db.relationship('User', foreign_keys=[user_id])


class TokenSchema(Schema):
    id = fields.Integer(dump_only=True)
    user_id = fields.Integer()
    access_token = fields.String()
    refresh_token = fields.String()
