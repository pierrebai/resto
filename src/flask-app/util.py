import json
import traceback
import enum
from functools import wraps

import marshmallow


############################################################################
#
# Event parameters extraction.


def extract_event_param(event: dict, param_name: str, default=None):
    """
    Extract a named parameters from the request event.
    The parameters can dig in sub-pieces of the event by separating each one with a slash.
    A default value can be provided if the parameter is not found, defaulting to None.
    """
    return extract_dict_data(event, param_name, default)


def extract_dict_data(top_dict: dict, data_path: str, default=None):
    """
    Extract a data item from a series of nested dictionaries following the given key path.
    The parameters can dig in sub-dictionraries of the given dictionary by separating each
    name key with a slash.
    A default value can be provided if the keys are not found, defaulting to None.
    """
    value = top_dict
    keys = data_path.split('/')
    for k in keys:
        try:
            value = value[k]
        except:
            return default
    return value


############################################################################
#
# URL path parameters extraction.


def extract_path_param(event, param_name, default=None):
    """
    Extract a named parameters from the request URL path.
    A default value can be provided if the parameter is not found, defaulting to None.
    """
    return extract_event_param(event, f'pathParameters/{param_name}', default=default)


############################################################################
#
# URL parameters extraction.


def extract_url_param(event, param_name, default=None):
    """
    Extract a named parameters from the request URL.
    A default value can be provided if the parameter is not found, defaulting to None.
    """
    return extract_event_param(event, f'queryStringParameters/{param_name}', default=default)


############################################################################
#
# Headers parameters extraction.


def extract_header_param(event, param_name, default=None):
    """
    Extract a named parameters from the request headers.
    A default value can be provided if the parameter is not found, defaulting to None.
    """
    return extract_event_param(event, f'headers/{param_name}', default=default)


############################################################################
#
# JSON body parameters extraction.


def extract_json_body(event) -> dict:
    """
    Decode the event body as a dictionary.
    """
    body = extract_event_param(event, 'body')
    if body is None:
        raise ExpectedProblemException('Missing POST JSON body.', ErrorCode.NO_JSON_BODY)

    try:
        json_dict = json.loads(body)
    except Exception as e:
        raise ExpectedProblemException(f'Invalid POST JSON body: {body}. (Error: {e})', ErrorCode.INVALID_JSON_BODY)

    return json_dict


def extract_json_body_params(event, expected_params: dict) -> dict:
    """
    Decode the event body as a dictionary and extract the expected parameters.
    If the parameter is not found, use the value given in expected_params.
    If the expected param is None, then the parameters is required and its absence
    will cause an error.
    """
    json_dict = extract_json_body(event)
    received_params = {}
    missing_params = []
    for k,v in expected_params.items():
        if k in json_dict:
            received_params[k] = json_dict[k]
        elif v is None:
            missing_params.append(k)
        else:
            received_params[k] = v

    if missing_params:
        raise ExpectedProblemException(f'Missing parameters: {missing_params}.', ErrorCode.MISSING_PARAMS)

    return received_params


def unmarshall_json_body_params(event, schema) -> dict:
    """
    Decode the event body as a dictionary from the given marshmallow schema.
    """
    json_dict = extract_json_body(event)
    try:
        return schema.load(json_dict)
    except marshmallow.exceptions.ValidationError as exc:
        raise ExpectedProblemException(exc.messages, ErrorCode.INVALID_PARAMS)


############################################################################
#
# Web request result helpers.

def return_body(body: dict, status_code: int, headers: dict = None) -> dict:
    """
    Create the dictionary to return the body of a web request, with optional headers.
    """
    # All these dictionary entries are specified by the AWS SAM framework.
    result = { 'statusCode': status_code, 'body': json.dumps(body) }

    # Note: normally, we would allow configuring the CORS headers.
    result_headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': '*',        
        'Access-Control-Allow-Methods': '*',
        'Access-Control-Allow-Credentials': 'true',
    }

    # Add request-specific headers.
    if headers:
        result_headers.update(headers)
    
    result['headers'] = result_headers
    
    return result

def return_success_body(body: dict, status_code: int = 200, headers: dict = None) -> dict:
    """
    Create the dictionary to return the body of a successful web request.
    """
    return return_body(body, status_code, headers)


def return_success_body_with_location(body: dict, location: str, status_code: int = 201) -> dict:
    """
    Create the dictionary to return the body and a location URL of a successful web request.
    """
    return return_success_body(body, status_code = status_code, headers = { 'location': location })


############################################################################
#
# Web request error helpers.


@enum.unique
class ErrorCode(enum.Enum):
    """
    Error codes that can be returned to the front-end.
    These are always returned in textual form in the error_code entry of the returned JSON.
    """
    OBJECT_NOT_FOUND = enum.auto()

    NOT_IMPLEMENTED = enum.auto()

    NOT_AUTHORIZED = enum.auto()
    INVALID_CREDENTIAL = enum.auto()
    AUTH_TOKEN_EXPIRED = enum.auto()

    INVALID_URI = enum.auto()
    INVALID_HTTP_METHOD = enum.auto()

    NO_JSON_BODY = enum.auto()
    INVALID_JSON_BODY = enum.auto()
    
    INVALID_PARAMS = enum.auto()
    MISSING_PARAMS = enum.auto()


def return_error(message: str, error_code: ErrorCode, status_code: int = 400) -> dict:
    """
    Create the dictionary to return an error to a web request.
    """
    return return_body({ 'message': message, 'error_code': error_code.name }, status_code)


def return_exception(limit=None, status_code: int = 400) -> dict:
    """
    Create the dictionary to return the stack trace of the current exception to a web request.
    """
    trace = traceback.format_exc(limit=limit).split('\n')
    body = {
        'message': "Internal error: an unhandled exception occurred during processing.",
        'trace': trace
    }
    return return_body(body, status_code)


############################################################################
#
# Exception trapping helpers.


class ExpectedProblemException(Exception):
    """
    An exception class to be thrown to stop the execution of the end-point
    with an error message and error code.

    Allows to abort the end-point from deep within function calls. No stack will be printed,
    only the error message is returned to the web caller.
    """
    def __init__(self, message, error_code: ErrorCode, status_code: int = 400):
        Exception.__init__(self, message)
        self.status_code = status_code
        self.error_code = error_code


def catch_exceptions(fn):
    """
    Decorator used to catch exceptions escaping from an AWS
    Lambda function end-point and return an error message with
    the stack trace.
    TODO: maybe we want to turn off the stack trace in prod?
    """
    def wrapped(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except ExpectedProblemException as e:
            return return_error(str(e), e.error_code, e.status_code)
        except:
            return return_exception()
    return wraps(fn)(wrapped)


############################################################################
#
# HTTP method helper.


def dispatch_to_http_handler(event, context, get_handler=None, post_handler=None, put_handler=None, delete_handler=None) -> dict:
    """
    Dispatch to the correct sub-handler depending if it is a GET, POST, PUT or DELETE.
    Return an error if it is not a supported HTTP method.
    """
    avail = {
        'GET': get_handler,
        'POST': post_handler,
        'PUT': put_handler,
        'DELETE': delete_handler,
    }
    method = extract_event_param(event, 'httpMethod')
    if method in avail and avail[method]:
        return avail[method](event, context)
    else:
        return return_error('Invalid HTTP Method', ErrorCode.INVALID_HTTP_METHOD)

