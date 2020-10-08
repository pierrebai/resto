from flask_apispec import marshal_with, use_kwargs
from flask_apispec import doc as more_doc
from marshmallow import Schema


############################################################################
#
# Registering with swagger

_registered_functions = []
_error_schema = None
_error_codes = '400 403'


def set_error_schema(error_schema: Schema, error_codes = '400 403'):
    """
    Sets the schema and error codes used to return errors.
    Since most functions use a common error schema, it is set only once.
    """
    global _error_schema
    _error_schema = error_schema
    global _error_codes
    _error_codes = error_codes


def swag(input: Schema = None, output: Schema = None, doc: str = None, tag: str = None, success: int = 200):
    """
    Decorator to automatically registers the function to the swagger docs
    and add schema for input JSON, output JSON, success code and error codes.
    Also adds the documentation and a tag to group related end-points together.
    """
    def decorator(func):
        # Input JSON, if any.
        if input:
            func = use_kwargs(input, apply=False)(func)

        # Note: if output is None, it merely documents the success code.
        func = marshal_with(output, code = success)(func)

        # Error schema and codes when we return an error.
        global _error_schema
        global _error_codes
        if _error_schema:
            func = marshal_with(_error_schema, code = _error_codes)(func)

        # Optional documentation.
        if doc:
            func = more_doc(description=doc)(func)

        # Optional tagging to group related end-points.
        if tag:
            func = more_doc(tags=[tag])(func)

        global _registered_functions
        _registered_functions.append(func)
        return func
    return decorator


def register_with_swagger_docs(docs):
    """
    Do the real registration with the swagger docs.
    Cannot be done while the function is not yet fully declared.
    """
    for f in _registered_functions:
        docs.register(f)

