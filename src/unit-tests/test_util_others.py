import unittest
from unittest.mock import Mock, patch

import traceback

import  util


class TestUtilOthers(unittest.TestCase):

    def test_catch_exceptions_unknown_exception(self):
        """
        The goal of the test is to verify that the catch_exceptions decorator
        successfully catches exception and return the correct dictionary.
        """

        @util.catch_exceptions
        def fail():
            raise Exception('oops')

        result = fail()
        self.assertEqual(400, result['statusCode'])
        self.assertIn('Internal error: an unhandled exception occurred during processing', result['body'])


    def test_catch_exceptions_expected_problem(self):
        """
        The goal of the test is to verify that the catch_exceptions decorator
        successfully catches exception and return the correct dictionary.
        """

        @util.catch_exceptions
        def fail():
            raise util.ExpectedProblemException('oops', util.ErrorCode.AUTH_TOKEN_EXPIRED, status_code=401)

        result = fail()
        self.assertEqual(401, result['statusCode'])
        self.assertIn('oops', result['body'])
        self.assertIn('AUTH_TOKEN_EXPIRED', result['body'])


    def test_dispatch_to_http_handler(self):
        """
        The goal of the test is to verify that dispatch_to_http_handler()
        calls the correct function for GET, POST and PUT.
        """
        def get_handler(event, context):
            return { 'get': 'success '}

        def post_handler(event, context):
            return { 'post': 'success '}

        def put_handler(event, context):
            return { 'put': 'success '}

        def delete_handler(event, context):
            return { 'delete': 'success '}

        event = { 'httpMethod': 'GET' }
        context = None
        self.assertEqual({ 'get': 'success '}, util.dispatch_to_http_handler(
            event, context, get_handler=get_handler))

        event = { 'httpMethod': 'GET' }
        context = None
        self.assertEqual({ 'get': 'success '}, util.dispatch_to_http_handler(
            event, context, get_handler=get_handler, post_handler=post_handler, put_handler=put_handler))

        event = { 'httpMethod': 'POST' }
        context = None
        self.assertEqual({ 'post': 'success '}, util.dispatch_to_http_handler(
            event, context, get_handler=get_handler, post_handler=post_handler, put_handler=put_handler))

        event = { 'httpMethod': 'PUT' }
        context = None
        self.assertEqual({ 'put': 'success '}, util.dispatch_to_http_handler(
            event, context, get_handler=get_handler, post_handler=post_handler, put_handler=put_handler))

        event = { 'httpMethod': 'DELETE' }
        context = None
        self.assertEqual({ 'delete': 'success '}, util.dispatch_to_http_handler(
            event, context, delete_handler=delete_handler))

        event = { 'httpMethod': 'WONKA' }
        context = None
        result = util.dispatch_to_http_handler(event, context)
        self.assertEqual(400, result['statusCode'])
        self.assertIn('Invalid HTTP Method', result['body'])


if __name__ == '__main__':
    unittest.main()

