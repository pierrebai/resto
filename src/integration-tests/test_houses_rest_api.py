import unittest
from unittest.mock import Mock, patch

from resto import Expected, Method, Config
from prepare_login import prepare_login_for_read_tests, prepare_login_for_write_tests
from order_tests import load_ordered_tests


# This orders the tests to be run in the order they were declared.
# It uses the unittest load_tests protocol.
load_tests = load_ordered_tests


class TestHousesRestApi(unittest.TestCase):

    ############################################################################
    #
    # /houses GET tests

    def test_houses(self):
        """
        The goal of the test is to verify that the /houses end-point
        returns the list of existing houses.
        """
        cfg = Config()
        self.maxDiff = 32000

        in_headers = prepare_login_for_read_tests(cfg)

        exp = Expected(
            url = '/houses',
            method = Method.GET,
            in_headers = in_headers,
            out_json = {
                "total_item_count": 3,
                "houses": [
                    {
                        "id": 1,
                        "name": "Frank's house",
                    },
                    {
                        "id": 2,
                        "name": "Janet's house",
                    },
                    {
                        "id": 3,
                        "name": "Marcy's house",
                    },
                ],
            }
        )
        diff = exp.call(cfg)
        self.assertEqual({}, diff)


    def test_houses_fail_no_auth(self):
        """
        The goal of the test is to verify that the /houses end-point
        fails when the user is not logged in.
        """
        cfg = Config()
        self.maxDiff = 32000

        exp = Expected(
            url = '/houses',
            method = Method.GET,
            out_json = {
                'message': 'Invalid login.',
                'error_code': 'INVALID_CREDENTIAL',
            },
            status_code = 403
        )
        diff = exp.call(cfg)
        self.assertEqual({}, diff)


    def test_houses_single(self):
        """
        The goal of the test is to verify that the /houses/{id} end-point
        returns the expected house.
        """
        cfg = Config()
        self.maxDiff = 32000

        in_headers = prepare_login_for_read_tests(cfg)

        houses = [
            {
                "id": 1,
                "name": "Frank's house",
            },
            {
                "id": 2,
                "name": "Janet's house",
            },
            {
                "id": 3,
                "name": "Marcy's house",
            },
        ]

        for house in houses:
            id = house['id']
            exp = Expected(
                url = f'/houses/{id}',
                method = Method.GET,
                in_headers = in_headers,
                out_json = { 'house': house }
            )
            diff = exp.call(cfg)
            self.assertEqual({}, diff)


    def test_houses_single_fail_no_auth(self):
        """
        The goal of the test is to verify that the /houses/{id} end-point
        fails when the user is not logged in.
        """
        cfg = Config()
        self.maxDiff = 32000

        exp = Expected(
            url = '/houses/1',
            method = Method.GET,
            out_json = {
                'message': 'Invalid login.',
                'error_code': 'INVALID_CREDENTIAL',
            },
            status_code = 403
        )
        diff = exp.call(cfg)
        self.assertEqual({}, diff)


    def test_houses_single_fail_not_found(self):
        """
        The goal of the test is to verify that the /houses/{id} end-point
        returns the expected error when the house id is not found.
        """
        cfg = Config()
        self.maxDiff = 32000

        in_headers = prepare_login_for_read_tests(cfg)

        exp = Expected(
            url = f'/houses/99',
            method = Method.GET,
            in_headers = in_headers,
            out_json = { 'message': 'House with id 99 does not exist.', 'error_code': 'OBJECT_NOT_FOUND' },
            status_code=404
        )
        diff = exp.call(cfg)
        self.assertEqual({}, diff)


    ############################################################################
    #
    # /houses POST tests

    def test_houses_create_successful(self):
        """
        The goal of the test is to verify that the /houses end-point
        can create a new house when POST and return the correct info.
        """
        cfg = Config()
        self.maxDiff = 32000

        in_headers = prepare_login_for_write_tests(cfg)

        in_house = {
            "name": "Susan's House",
        }

        out_house = {
            "house": {
                "id": 4,
                "name": "Susan's House",
            }
        }

        exp = Expected(
            url = f'/houses',
            method = Method.POST,
            in_json = in_house,
            in_headers = in_headers,
            out_json = out_house,
            out_headers = { 'Location': f'{cfg.base_url}/houses/4' },
            status_code = 201
        )
        diff = exp.call(cfg)
        self.assertEqual({}, diff)


    def test_houses_create_fail_no_auth(self):
        """
        The goal of the test is to verify that the /houses POST end-point
        fails when the user is not logged in.
        """
        cfg = Config()
        self.maxDiff = 32000

        exp = Expected(
            url = '/houses',
            method = Method.POST,
            out_json = {
                'message': 'Invalid login.',
                'error_code': 'INVALID_CREDENTIAL',
            },
            status_code = 403
        )
        diff = exp.call(cfg)
        self.assertEqual({}, diff)


    def test_houses_create_fail_no_name(self):
        """
        The goal of the test is to verify that the /houses end-point
        fail to create a new house when no name was provided.
        """
        cfg = Config()
        self.maxDiff = 32000

        in_headers = prepare_login_for_write_tests(cfg)

        in_house = {
            "name": "",
        }

        exp = Expected(
            url = f'/houses',
            method = Method.POST,
            in_json = in_house,
            in_headers = in_headers,
            out_json = { 'message': '~name', 'error_code': 'INVALID_PARAMS'},
            status_code = 400
        )
        diff = exp.call(cfg)
        self.assertEqual({}, diff)


    ############################################################################
    #
    # /houses/id PUT tests

    def test_houses_update_successful(self):
        """
        The goal of the test is to verify that the /houses end-point
        can update a house when PUT and return the correct info.
        """
        cfg = Config()
        self.maxDiff = 32000

        in_headers = prepare_login_for_write_tests(cfg)

        in_house = {
            "name": "Susan's Castle",
        }

        out_house = {
            "house": {
                "id": 4,
                "name": "Susan's Castle",
            }
        }

        exp = Expected(
            url = f'/houses/4',
            method = Method.PUT,
            in_json = in_house,
            in_headers = in_headers,
            out_json = out_house,
            out_headers = { 'Location': f'{cfg.base_url}/houses/4' },
            status_code = 200
        )
        diff = exp.call(cfg)
        self.assertEqual({}, diff)


    def test_houses_update_successful_same_name(self):
        """
        The goal of the test is to verify that the /houses end-point
        can update a house even if the supplied names are unchanged
        when PUT and return the correct info.
        """
        cfg = Config()
        self.maxDiff = 32000

        in_headers = prepare_login_for_write_tests(cfg)

        in_house = {
            "name": "Susan's Castle",
        }

        out_house = {
            "house": {
                "id": 4,
                "name": "Susan's Castle",
            }
        }

        exp = Expected(
            url = f'/houses/4',
            method = Method.PUT,
            in_json = in_house,
            in_headers = in_headers,
            out_json = out_house,
            out_headers = { 'Location': f'{cfg.base_url}/houses/4' },
            status_code = 200
        )
        diff = exp.call(cfg)
        self.assertEqual({}, diff)


    def test_houses_update_create_fail_no_auth(self):
        """
        The goal of the test is to verify that the /houses PUT end-point
        fails when the user is not logged in.
        """
        cfg = Config()
        self.maxDiff = 32000

        exp = Expected(
            url = '/houses/4',
            method = Method.PUT,
            out_json = {
                'message': 'Invalid login.',
                'error_code': 'INVALID_CREDENTIAL',
            },
            status_code = 403
        )
        diff = exp.call(cfg)
        self.assertEqual({}, diff)


    def test_houses_update_fail_no_name(self):
        """
        The goal of the test is to verify that the /houses end-point
        fail to update a new house when no name was provided.
        """
        cfg = Config()
        self.maxDiff = 32000

        in_headers = prepare_login_for_write_tests(cfg)

        in_house = {
            "name": "",
        }

        exp = Expected(
            url = f'/houses/4',
            method = Method.PUT,
            in_json = in_house,
            in_headers = in_headers,
            out_json = { 'message': '~name', 'error_code': 'INVALID_PARAMS'},
            status_code = 400
        )
        diff = exp.call(cfg)
        self.assertEqual({}, diff)


    def test_houses_update_fail_not_found(self):
        """
        The goal of the test is to verify that the /houses end-point
        fail to update a non-existing house.
        """
        cfg = Config()
        self.maxDiff = 32000

        in_headers = prepare_login_for_write_tests(cfg)

        in_house = {
            "name": "Rollers",
        }

        exp = Expected(
            url = f'/houses/99',
            method = Method.PUT,
            in_json = in_house,
            in_headers = in_headers,
            out_json = { 'message': 'House with id 99 does not exist.', 'error_code': 'OBJECT_NOT_FOUND'},
            status_code = 404
        )
        diff = exp.call(cfg)
        self.assertEqual({}, diff)
        

    ############################################################################
    #
    # /houses/id DELETE tests

    def test_houses_delete_successful(self):
        """
        The goal of the test is to verify that the /houses DELETE end-point
        can delete a house.
        """
        cfg = Config()
        self.maxDiff = 32000

        in_headers = prepare_login_for_write_tests(cfg)

        exp = Expected(
            url = f'/houses/4',
            method = Method.DELETE,
            in_headers = in_headers,
            out_json = { 'message': 'House 4 deletion successful.' },
            status_code = 200
        )
        diff = exp.call(cfg)
        self.assertEqual({}, diff)

        # Verify the house is not longer present.
        exp = Expected(
            url = f'/houses/4',
            method = Method.GET,
            in_headers = in_headers,
            out_json = { 'message': f'House with id 4 does not exist.', 'error_code': 'OBJECT_NOT_FOUND' },
            status_code=404
        )
        diff = exp.call(cfg)
        self.assertEqual({}, diff)


    def test_houses_delete_fail_no_auth(self):
        """
        The goal of the test is to verify that the /houses DELETE end-point
        fails when the user is not logged in.
        """
        cfg = Config()
        self.maxDiff = 32000

        exp = Expected(
            url = f'/houses/30',
            method = Method.DELETE,
            out_json = { 'message': 'Invalid login.', 'error_code': 'INVALID_CREDENTIAL' },
            status_code = 403
        )
        diff = exp.call(cfg)
        self.assertEqual({}, diff)


    def test_houses_delete_fail_not_found(self):
        """
        The goal of the test is to verify that the /houses DELETE end-point
        fails when the house does not exist.
        """
        cfg = Config()
        self.maxDiff = 32000

        in_headers = prepare_login_for_read_tests(cfg)

        exp = Expected(
            url = f'/houses/99',
            method = Method.DELETE,
            in_headers = in_headers,
            out_json = { 'message': 'House with id 99 does not exist.', 'error_code': 'OBJECT_NOT_FOUND'},
            status_code = 404
        )
        diff = exp.call(cfg)
        self.assertEqual({}, diff)


if __name__ == '__main__':
    unittest.main()

