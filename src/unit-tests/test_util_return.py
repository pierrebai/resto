import unittest
from unittest.mock import Mock, patch

import traceback

import  util


class TestUtilReturn(unittest.TestCase):

    def test_return_error(self):
        """
        The goal of the test is to verify that return_error()
        returns the correct data in the returned ditionary for errors.
        """
        self.assertEqual(
            {
                'body': '{"message": "msg", "error_code": "OBJECT_NOT_FOUND"}',
                'statusCode': 400,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Headers': '*',        
                    'Access-Control-Allow-Methods': '*',
                    'Access-Control-Allow-Credentials': 'true',
                },
            }, util.return_error('msg', util.ErrorCode.OBJECT_NOT_FOUND))

        self.assertEqual(
            {
                'body': '{"message": "msg", "error_code": "INVALID_URI"}',
                'statusCode': 404,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Headers': '*',        
                    'Access-Control-Allow-Methods': '*',
                    'Access-Control-Allow-Credentials': 'true',
                },
            }, util.return_error('msg', util.ErrorCode.INVALID_URI, 404))

    
    @patch('traceback.format_exc')
    def test_return_exception(self, mock_format_exc):
        """
        The goal of the test is to verify that return_exception()
        returns the correct data in the returned ditionary for exceptions.
        """
        mock_format_exc.return_value = "stack trace"
        try:
            raise Exception('oh no')
        except:
            self.assertEqual(            {
                'body': '{"message": "Internal error: an unhandled exception occurred during processing.", "trace": ["stack trace"]}',
                'statusCode': 400,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Headers': '*',        
                    'Access-Control-Allow-Methods': '*',
                    'Access-Control-Allow-Credentials': 'true',
                },
            }, util.return_exception())


    def test_return_success_body(self):
        """
        The goal of the test is to verify that return_success_body()
        returns the correct data in the returned ditionary for successful requests.
        """
        self.assertEqual(
            {
                'body': '{"key": "value"}',
                'statusCode': 200,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Headers': '*',        
                    'Access-Control-Allow-Methods': '*',
                    'Access-Control-Allow-Credentials': 'true',
                },
            }, util.return_success_body({'key': 'value'}))

        self.assertEqual(
            {
                'body': '{"key": "value"}',
                'statusCode': 200,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Headers': '*',        
                    'Access-Control-Allow-Methods': '*',
                    'Access-Control-Allow-Credentials': 'true',
                    'h1': 'v1',
                },
            }, util.return_success_body({'key': 'value'}, headers={'h1': 'v1'}))

        self.assertEqual(
            {
                'body': '{"key": "value"}',
                'statusCode': 201,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Headers': '*',        
                    'Access-Control-Allow-Methods': '*',
                    'Access-Control-Allow-Credentials': 'true',
                    'h1': 'v1'
                },
            }, util.return_success_body({'key': 'value'}, 201, headers={'h1': 'v1'}))


    def test_return_success_body_with_location(self):
        """
        The goal of the test is to verify that return_success_body_with_location()
        returns the correct data in the returned ditionary for successful requests
        that created a new object in the DB.
        """
        self.assertEqual(
            {
                'body': '{"key": "value"}',
                'statusCode': 201,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Headers': '*',        
                    'Access-Control-Allow-Methods': '*',
                    'Access-Control-Allow-Credentials': 'true',
                    'location': 'ici'
                },
            }, util.return_success_body_with_location({'key': 'value'}, 'ici'))


if __name__ == '__main__':
    unittest.main()

