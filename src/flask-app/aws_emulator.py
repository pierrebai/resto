import json

from flask import Flask, request, Response


############################################################################
#
# Functions to take data from flask request convert them into the
# equivalent AWS Lambda event and context.
#
# Similarly, a function to convert a flask response into the equivalent
# AWS Lambda result format.
#
# This allows emulating the AWS Lambda using flask, which greatly
# speed up testing.


def get_event(**kwargs) -> dict:
    """
    Create a mock AWS event from the flask request.
    Convert the request method, body and URL parameters.
    """
    event = {
        'httpMethod': request.method,
    }
    if request.args:
        event['queryStringParameters'] = {}
        for k, v in request.args.items():
            event['queryStringParameters'][k] = v
    if request.headers:
        event['headers'] = {}
        for k, v in request.headers.items():
            event['headers'][k] = v
    if request.is_json:
        event['body'] = json.dumps(request.get_json())
    if kwargs:
        event['pathParameters'] = {}
        for k, v in kwargs.items():
            event['pathParameters'][k] = v
    return event


def get_context() -> dict:
    """
    Create a mock AWS context.
    """
    context = {
    }
    return context


def convert_result(result: dict):
    """
    Convert a AWS result dictionary to a flask response.
    Convert the body, status code and headers.
    """
    status_code = result['statusCode']
    body = result['body']
    headers = None
    if 'headers' in result:
        headers = result['headers']
    return Response(body, status=status_code, content_type='application/json', headers=headers)


