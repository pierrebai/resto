import enum

from marshmallow import Schema, fields, validate
from marshmallow_enum import EnumField

"""
This module declares schema classes to model the JSON received from (or sent to) the REST API.

It uses marshmallow to create the schema classes.
"""

"""
Re-usable required text field that is validated to not be empty.
"""
_NonEmptyString = fields.String(required=True, validate=validate.Length(min=1))


class WithIdPrimaryKey():
    """
    Schema base class with an id primary key that is dump-only.
    """
    id = fields.Int(dump_only=True)


class WithFirstLastName():
    """
    Schema base class with first and last name.
    Having it in common will allow having the same behaviour when filtering, searching.
    """
    first_name = _NonEmptyString
    last_name = _NonEmptyString


class Dog(WithIdPrimaryKey, WithFirstLastName, Schema):
    """
    Schema of a dog.
    """
    pass

class Dogs(Schema):
    """
    Schema representing a list of dogs.
    """
    dogs = fields.List(fields.Nested(Dog))


class OneDog(Schema):
    """
    Schema representing a single dog.
    """
    dog = fields.Nested(Dog)
    

class Login(Schema):
    """
    Schema to login.
    """
    email = fields.Email(required=True)
    cleartext_password = fields.String(data_key='password', load_only=True, required=True, validate=validate.Length(min=1))


class AuthToken(Schema):
    """
    Schema representing the authorization token returned by login.
    """
    auth_token = _NonEmptyString


class LoginAuthToken(Schema):
    """
    Schema representing the authorization token returned by login.
    """
    auth_token = _NonEmptyString
    dog = fields.Nested(Dog)


class House(WithIdPrimaryKey, Schema):
    """
    Schema of houses.
    """
    name = _NonEmptyString
        

class Houses(Schema):
    """
    Schema representing a list of houses.
    """
    houses = fields.List(fields.Nested(House))


class OneHouse(Schema):
    """
    Schema representing a single house.
    """
    house = fields.Nested(House)
    

class ExpectedError(Schema):
    """
    Schema representing an error returned by an end-point.
    """
    message = _NonEmptyString
    error_code = _NonEmptyString


