import unittest
from unittest.mock import Mock, patch

from resto import Expected, Method, Config
from prepare_login import clear_auth_cache, prepare_login_for_read_tests, prepare_login_for_write_tests
from order_tests import load_ordered_tests


# This orders the tests to be run in the order they were declared.
# It uses the unittest load_tests protocol.
load_tests = load_ordered_tests


class TestLogoutRestApi(unittest.TestCase):

    ############################################################################
    #
    # /logout POST tests

    def test_logout_successful(self):
        """
        The goal of the test is to verify that the /logout end-point
        can logout a user.
        """
        cfg = Config()
        self.maxDiff = 32000

        in_headers = prepare_login_for_read_tests(cfg)
        clear_auth_cache()

        out_logout = {
            'message': 'Logout successful.',
        }

        exp = Expected(
            url = '/logout',
            method = Method.POST,
            in_headers = in_headers,
            out_json = out_logout,
            status_code = 200
        )
        diff = exp.call(cfg)
        self.assertEqual({}, diff)

        clear_auth_cache()


    def test_logout_fail_no_auth_header(self):
        """
        The goal of the test is to verify that the /logout end-point
        fails when no token is provided in the headers.
        """
        cfg = Config()
        self.maxDiff = 32000

        out_logout = {
            'message': 'Invalid login.',
            'error_code': 'INVALID_CREDENTIAL',
        }

        exp = Expected(
            url = '/logout',
            method = Method.POST,
            out_json = out_logout,
            status_code = 403
        )
        diff = exp.call(cfg)
        self.assertEqual({}, diff)


    def test_logout_fail_empty_auth_header(self):
        """
        The goal of the test is to verify that the /logout end-point
        fails when the authorization header is empty.
        """
        cfg = Config()
        self.maxDiff = 32000

        in_headers = {
            'Authorization': ''
        }

        out_logout = {
            'message': 'Invalid login.',
            'error_code': 'INVALID_CREDENTIAL',
        }

        exp = Expected(
            url = '/logout',
            method = Method.POST,
            out_json = out_logout,
            status_code = 403
        )
        diff = exp.call(cfg)
        self.assertEqual({}, diff)


    def test_logout_fail_empty_bearer(self):
        """
        The goal of the test is to verify that the /logout end-point
        fails when the authorization header contains an empty bearer.
        """
        cfg = Config()
        self.maxDiff = 32000

        in_headers = {
            'Authorization': 'Bearer'
        }

        out_logout = {
            'message': 'Invalid login.',
            'error_code': 'INVALID_CREDENTIAL',
        }

        exp = Expected(
            url = '/logout',
            method = Method.POST,
            out_json = out_logout,
            status_code = 403
        )
        diff = exp.call(cfg)
        self.assertEqual({}, diff)


    def test_logout_fail_empty_auth_token(self):
        """
        The goal of the test is to verify that the /logout end-point
        fails when the authorization header contains an empty auth token.
        """
        cfg = Config()
        self.maxDiff = 32000

        # Note: note the extra space after bearer.
        #       That's the difference with the preceeding test.
        in_headers = {
            'Authorization': 'Bearer '
        }

        out_logout = {
            'message': 'Invalid login.',
            'error_code': 'INVALID_CREDENTIAL',
        }

        exp = Expected(
            url = '/logout',
            method = Method.POST,
            out_json = out_logout,
            status_code = 403
        )
        diff = exp.call(cfg)
        self.assertEqual({}, diff)


if __name__ == '__main__':
    unittest.main()

