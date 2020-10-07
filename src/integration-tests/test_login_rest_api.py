import unittest
from unittest.mock import Mock, patch

from resto import Expected, Method, Config
from prepare_login import prepare_login_for_read_tests, prepare_login_for_write_tests
from order_tests import load_ordered_tests


# This orders the tests to be run in the order they were declared.
# It uses the unittest load_tests protocol.
load_tests = load_ordered_tests


class TestLoginRestApi(unittest.TestCase):

    ############################################################################
    #
    # /login POST tests

    def test_login_successful(self):
        """
        The goal of the test is to verify that the /login end-point
        can login a user when POST and return the correct info.
        """
        cfg = Config()
        self.maxDiff = 32000

        in_login = {
            "email": "salomon_deed@example.com",
            "password": "abcdef",
        }

        out_login = {
            'auth_token': '*',
        }

        exp = Expected(
            url = '/login',
            method = Method.POST,
            in_json = in_login,
            out_json = out_login,
            status_code = 200
        )
        diff = exp.call(cfg)
        self.assertEqual({}, diff)


    def test_login_fail_bad_email(self):
        """
        The goal of the test is to verify that the /login end-point
        fail to login a user when the email is invalid.
        """
        cfg = Config()
        self.maxDiff = 32000

        in_login = {
            "email": "no-one@example.com",
            "password": "abcdef",
        }

        exp = Expected(
            url = '/login',
            method = Method.POST,
            in_json = in_login,
            out_json = { 'message': 'Invalid login.', 'error_code': 'INVALID_CREDENTIAL'},
            status_code = 403
        )
        diff = exp.call(cfg)
        self.assertEqual({}, diff)


    def test_login_fail_bad_password(self):
        """
        The goal of the test is to verify that the /login end-point
        fail to login a user when the email is invalid.
        """
        cfg = Config()
        self.maxDiff = 32000

        in_login = {
            "email": "salomon_deed@example.com",
            "password": "123456",
        }

        exp = Expected(
            url = '/login',
            method = Method.POST,
            in_json = in_login,
            out_json = { 'message': 'Invalid login.', 'error_code': 'INVALID_CREDENTIAL'},
            status_code = 403
        )
        diff = exp.call(cfg)
        self.assertEqual({}, diff)


    def test_login_fail_no_email(self):
        """
        The goal of the test is to verify that the /login end-point
        fail to login a user when no email was provided.
        """
        cfg = Config()
        self.maxDiff = 32000

        in_login = {
            "email": "",
            "password": "123456",
        }

        exp = Expected(
            url = '/login',
            method = Method.POST,
            in_json = in_login,
            out_json = { 'message': '~Not a valid email address', 'error_code': 'INVALID_PARAMS'},
            status_code = 400
        )
        diff = exp.call(cfg)
        self.assertEqual({}, diff)

    def test_login_fail_short_password(self):
        """
        The goal of the test is to verify that the /login end-point
        fail to login a user when the passwor is too short.
        """
        cfg = Config()
        self.maxDiff = 32000

        in_login = {
            "email": "salomon_deed@example.com",
            "password": "",
        }

        exp = Expected(
            url = '/login',
            method = Method.POST,
            in_json = in_login,
            out_json = { 'message': '~password', 'error_code': 'INVALID_PARAMS'},
            status_code = 400
        )
        diff = exp.call(cfg)
        self.assertEqual({}, diff)


if __name__ == '__main__':
    unittest.main()

