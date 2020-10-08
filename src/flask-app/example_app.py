import json

from flask import Flask

from aws_emulator import convert_result, get_event, get_context
from easy_swag import swag, set_error_schema, register_with_swagger_docs
import login
import schemas

import dogs, houses

app = Flask(__name__)


############################################################################
#
# Set the error schema used in function and documented in swagger doc.

set_error_schema(schemas.ExpectedError, '400, 403')


############################################################################
#
# Login URLs.


@app.route('/login', methods=['POST'])
@swag(input=schemas.Login, output=schemas.LoginAuthToken, doc='Login into the web app', tag='Authorization')
def login_handler(**kwargs):
    return convert_result(login.login_handler(get_event(), get_context()))


@app.route('/refresh_token', methods=['GET'])
@swag(output=schemas.AuthToken, doc='Refresh the authorization token', tag='Authorization')
def refresh_token_handler():
    return convert_result(login.refresh_token_handler(get_event(), get_context()))


@app.route('/logout', methods=['POST'])
@swag(doc='Logout of the web app', tag='Authorization')
def logout_handler():
    return convert_result(login.logout_handler(get_event(), get_context()))


############################################################################
#
# Dogs URLs.


@app.route('/dogs', methods=['GET'])
@swag(output=schemas.Dogs, doc='Retrieve all dogs', tag='dogs')
def dogs_get_handler():
    return convert_result(dogs.dogs_handler(get_event(), get_context()))


@app.route('/dogs', methods=['POST'])
@swag(input=schemas.Dog, success=201, doc='Create a new dog', tag='dogs')
def dogs_post_handler(**kwargs):
    return convert_result(dogs.dogs_handler(get_event(), get_context()))


@app.route('/dogs/<int:id>', methods=['GET'])
@swag(output=schemas.Dog, doc='Retrieve a dog by its id', tag='dogs')
def dogs_id_get_handler(id):
    return convert_result(dogs.dogs_handler(get_event(id=id), get_context()))


@app.route('/dogs/<int:id>', methods=['PUT'])
@swag(input=schemas.Dog, doc='Update an existing dog', tag='dogs')
def dogs_id_put_handler(id, **kwargs):
    return convert_result(dogs.dogs_handler(get_event(id=id), get_context()))


############################################################################
#
# Houses URLs.


@app.route('/houses', methods=['GET'])
@swag(output=schemas.Houses, doc='Retrieve all houses', tag='houses')
def houses_get_handler():
    return convert_result(houses.houses_handler(get_event(), get_context()))


@app.route('/houses', methods=['POST'])
@swag(input=schemas.House, success=201, doc='Create a new house', tag='houses')
def houses_post_handler(**kwargs):
    return convert_result(houses.houses_handler(get_event(), get_context()))


@app.route('/houses/<int:id>', methods=['GET'])
@swag(output=schemas.OneHouse, doc='Retrieve one house by its id', tag='houses')
def houses_id_get_handler(id):
    return convert_result(houses.houses_handler(get_event(id=id), get_context()))


@app.route('/houses/<int:id>', methods=['PUT'])
@swag(input=schemas.House, doc='Update an existing house by its id', tag='houses')
def houses_id_put_handler(id, **kwargs):
    return convert_result(houses.houses_handler(get_event(id=id), get_context()))


@app.route('/houses/<int:id>', methods=['DELETE'])
@swag(doc='Delete an existing house by its id')
def houses_id_delete_handler(id):
    return convert_result(houses.houses_handler(get_event(id=id), get_context()))


############################################################################
#
# CORS Headers

@app.after_request
def after_request(response):
    headers_to_add = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': '*',
        'Access-Control-Allow-Methods': '*',
        'Access-Control-Allow-Credentials': 'true',
    }
    for header, value in headers_to_add.items():
        if header not in response.headers:
            response.headers.add(header, value)
    return response


############################################################################
#
# Swagger

from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from flask_apispec.extension import FlaskApiSpec


def enum_to_properties(self, field, **kwargs):
    """
    Add an OpenAPI extension for marshmallow_enum.EnumField instances
    """
    import marshmallow_enum
    if isinstance(field, marshmallow_enum.EnumField):
        return {'type': 'string', 'enum': [m.name for m in field.enum]}
    return {}


marshmallow_plugin = MarshmallowPlugin()

app.config.update({
    'APISPEC_SPEC': APISpec(
        title='example-web-app',
        version='v1',
        plugins=[marshmallow_plugin],
        openapi_version='2.0'
    ),
    'APISPEC_SWAGGER_URL': '/swagger/',
})

marshmallow_plugin.converter.add_attribute_function(enum_to_properties)
docs = FlaskApiSpec(app)
register_with_swagger_docs(docs)


############################################################################
#
# Entry-point.

def main():
    from werkzeug.serving import WSGIRequestHandler
    WSGIRequestHandler.protocol_version = "HTTP/1.1"
    app.run(port=3000)


if __name__ == '__main__':
    main()
