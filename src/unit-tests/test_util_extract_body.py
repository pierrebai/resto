import unittest
from unittest.mock import Mock, patch

import  util


class TestUtilExtractBody(unittest.TestCase):

    def test_extract_json_body(self):
        """
        The goal of the test is to verify that extract_json_body()
        extracts the JSON data from the body of the web event.

        It also verifies that it raises the expected exception when a problem occurs.
        """
        with self.assertRaises(util.ExpectedProblemException):
            util.extract_json_body(None)

        with self.assertRaises(util.ExpectedProblemException):
            util.extract_json_body(1)

        with self.assertRaises(util.ExpectedProblemException):
            util.extract_json_body({'body': None})

        with self.assertRaises(util.ExpectedProblemException):
            util.extract_json_body({'body': 1})

        with self.assertRaises(util.ExpectedProblemException):
            util.extract_json_body({'body': '{ [ "not quite" }'})

        self.assertEqual({ "json_key": "json_value" }, util.extract_json_body({'body': '{ "json_key": "json_value" }'}))


    def test_extract_json_body_params(self):
        """
        The goal of the test is to verify that extract_json_body_params()
        extracts and validates the expected parameters from the JSON body.

        It verifies that it raises an exception for missing required params.

        It verifies that it fills default values for missing optional params.
        """
        expected_params = {
            "req_param1": None,
            "req_param2": None,
            "opt_param1": "def_value",
        }
        with self.assertRaises(util.ExpectedProblemException):
            util.extract_json_body_params(None, expected_params)

        with self.assertRaises(util.ExpectedProblemException):
            util.extract_json_body_params(1, expected_params)

        with self.assertRaises(util.ExpectedProblemException):
            util.extract_json_body_params({'body': None}, expected_params)

        mock_body_missing_params = { 'body': '{ "json_key": "json_value" }' }
        with self.assertRaises(util.ExpectedProblemException):
            params = util.extract_json_body_params(mock_body_missing_params, expected_params)

        mock_body_missing_opt_param = { 'body': '{ "req_param1": "req1", "req_param2": "req2" }' }
        params = util.extract_json_body_params(mock_body_missing_opt_param, expected_params)
        self.assertEqual( {
            "req_param1": "req1",
            "req_param2": "req2",
            "opt_param1": "def_value",
        }, params)

        mock_body_all_param = { 'body': '{ "req_param1": "req1", "req_param2": "req2", "opt_param1": "opt1" }' }
        params = util.extract_json_body_params(mock_body_all_param, expected_params)
        self.assertEqual( {
            "req_param1": "req1",
            "req_param2": "req2",
            "opt_param1": "opt1",
        }, params)


if __name__ == '__main__':
    unittest.main()

