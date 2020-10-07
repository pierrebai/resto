import unittest
from unittest.mock import Mock, patch

from marshmallow import Schema, fields

import  util


class TestUtilUnmarshall(unittest.TestCase):

    def test_unmarshall_json_body_params(self):
        """
        The goal of the test is to verify that unmarshall_json_body_params()
        extracts and validates the schema from the JSON body.

        It verifies that it raises an exception for missing required params.

        It verifies that it fills default values for missing optional params.
        """
        class MySchema(Schema):
            req_param1 = fields.String(required=True)
            req_param2 = fields.String(required=True)
            opt_param1 = fields.String(missing="def_value")

        with self.assertRaises(util.ExpectedProblemException):
            util.unmarshall_json_body_params(None, MySchema())

        with self.assertRaises(util.ExpectedProblemException):
            util.unmarshall_json_body_params(1, MySchema())

        with self.assertRaises(util.ExpectedProblemException):
            util.unmarshall_json_body_params({'body': None}, MySchema())

        mock_body_missing_params = { 'body': '{ "json_key": "json_value" }' }
        with self.assertRaises(util.ExpectedProblemException):
            params = util.unmarshall_json_body_params(mock_body_missing_params, MySchema())

        mock_body_missing_opt_param = { 'body': '{ "req_param1": "req1", "req_param2": "req2" }' }
        params = util.unmarshall_json_body_params(mock_body_missing_opt_param, MySchema())
        self.assertEqual( {
            "req_param1": "req1",
            "req_param2": "req2",
            "opt_param1": "def_value",
        }, params)

        mock_body_all_param = { 'body': '{ "req_param1": "req1", "req_param2": "req2", "opt_param1": "opt1" }' }
        params = util.unmarshall_json_body_params(mock_body_all_param, MySchema())
        self.assertEqual( {
            "req_param1": "req1",
            "req_param2": "req2",
            "opt_param1": "opt1",
        }, params)


if __name__ == '__main__':
    unittest.main()

