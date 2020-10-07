import unittest
from unittest.mock import Mock, patch

from resto import Expected, Method, Config
from prepare_login import prepare_login_for_read_tests, prepare_login_for_write_tests
from order_tests import load_ordered_tests


# This orders the tests to be run in the order they were declared.
# It uses the unittest load_tests protocol.
load_tests = load_ordered_tests


class TestDogsRestApi(unittest.TestCase):

    ############################################################################
    #
    # /dogs GET tests

    def test_dogs(self):
        """
        The goal of the test is to verify that the /dogs end-point
        returns the list of existing dogs.
        """
        cfg = Config()
        self.maxDiff = 32000

        in_headers = prepare_login_for_read_tests(cfg)

        exp = Expected(
            url = '/dogs',
            method = Method.GET,
            in_headers = in_headers,
            out_json = {
                "total_item_count": 3,
                "dogs": [
                    {
                        "id": 1,
                        "first_name": "Blacky",
                        "last_name": "Doggy",
                    },
                    {
                        "id": 2,
                        "first_name": "Prancer",
                        "last_name": "Labrador",
                    },
                    {
                        "id": 3,
                        "first_name": "Fluffy",
                        "last_name": "Hair",
                    },
                ],
            },
        )
        diff = exp.call(cfg)
        self.assertEqual({}, diff)


    def test_dogs_fail_no_auth(self):
        """
        The goal of the test is to verify that the /dogs end-point
        fails when the user is not logged in.
        """
        cfg = Config()
        self.maxDiff = 32000

        exp = Expected(
            url = '/dogs',
            method = Method.GET,
            out_json = {
                'message': 'Invalid login.',
                'error_code': 'INVALID_CREDENTIAL',
            },
            status_code = 403
        )
        diff = exp.call(cfg)
        self.assertEqual({}, diff)


    def test_dogs_single(self):
        """
        The goal of the test is to verify that the /dogs/{id} end-point
        returns the expected dog.
        """
        cfg = Config()
        self.maxDiff = 32000

        in_headers = prepare_login_for_read_tests(cfg)

        dogs = [
            {
                "id": 1,
                "first_name": "Blacky",
                "last_name": "Doggy",
            },
            {
                "id": 2,
                "first_name": "Prancer",
                "last_name": "Labrador",
            },
        ]

        for dog in dogs:
            id = dog['id']
            exp = Expected(
                url = f'/dogs/{id}',
                method = Method.GET,
                in_headers = in_headers,
                out_json = { 'dog': dog }
            )
            diff = exp.call(cfg)
            self.assertEqual({}, diff)


    def test_dogs_single_fail_no_auth(self):
        """
        The goal of the test is to verify that the /dogs/{id} end-point
        fails when the user is not logged in.
        """
        cfg = Config()
        self.maxDiff = 32000

        exp = Expected(
            url = '/dogs/1',
            method = Method.GET,
            out_json = {
                'message': 'Invalid login.',
                'error_code': 'INVALID_CREDENTIAL',
            },
            status_code = 403
        )
        diff = exp.call(cfg)
        self.assertEqual({}, diff)


    def test_dogs_single_fail_not_found(self):
        """
        The goal of the test is to verify that the /dogs/{id} end-point
        returns the expected error when the dog id is not found.
        """
        cfg = Config()
        self.maxDiff = 32000

        in_headers = prepare_login_for_read_tests(cfg)

        exp = Expected(
            url = f'/dogs/99',
            method = Method.GET,
            in_headers = in_headers,
            out_json = { 'message': 'Dog with id 99 does not exist.', 'error_code': 'OBJECT_NOT_FOUND' },
            status_code=404
        )
        diff = exp.call(cfg)
        self.assertEqual({}, diff)


    ############################################################################
    #
    # /dogs POST tests

    def test_dogs_create_successful(self):
        """
        The goal of the test is to verify that the /dogs end-point
        can create a new dog when POST and return the correct info.
        """
        cfg = Config()
        self.maxDiff = 32000

        in_headers = prepare_login_for_write_tests(cfg)

        in_dog = {
            "first_name": "Wabby",
            "last_name": "Husky",
        }

        out_dog = {
            "dog": {
                "id": 4,
                "first_name": "Wabby",
                "last_name": "Husky",
            }
        }

        exp = Expected(
            url = f'/dogs',
            method = Method.POST,
            in_json = in_dog,
            in_headers = in_headers,
            out_json = out_dog,
            out_headers = { 'Location': f'{cfg.base_url}/dogs/4' },
            status_code = 201
        )
        diff = exp.call(cfg)
        self.assertEqual({}, diff)


    def test_dogs_create_fail_no_auth(self):
        """
        The goal of the test is to verify that the /dogs POST end-point
        fails when the user is not logged in.
        """
        cfg = Config()
        self.maxDiff = 32000

        exp = Expected(
            url = '/dogs',
            method = Method.POST,
            out_json = {
                'message': 'Invalid login.',
                'error_code': 'INVALID_CREDENTIAL',
            },
            status_code = 403
        )
        diff = exp.call(cfg)
        self.assertEqual({}, diff)


    def test_dogs_create_fail_no_first_name(self):
        """
        The goal of the test is to verify that the /dogs end-point
        fail to create a new dog when no first name was provided.
        """
        cfg = Config()
        self.maxDiff = 32000

        in_headers = prepare_login_for_write_tests(cfg)

        in_dog = {
            "first_name": "",
            "last_name": "Lasto",
        }

        exp = Expected(
            url = f'/dogs',
            method = Method.POST,
            in_json = in_dog,
            in_headers = in_headers,
            out_json = { 'message': '~first_name', 'error_code': 'INVALID_PARAMS'},
            status_code = 400
        )
        diff = exp.call(cfg)
        self.assertEqual({}, diff)


    def test_dogs_create_fail_no_last_name(self):
        """
        The goal of the test is to verify that the /dogs end-point
        fail to create a new dog when no last name was provided.
        """
        cfg = Config()
        self.maxDiff = 32000

        in_headers = prepare_login_for_write_tests(cfg)

        in_dog = {
            "first_name": "Ginger",
            "last_name": "",
        }

        exp = Expected(
            url = f'/dogs',
            method = Method.POST,
            in_json = in_dog,
            in_headers = in_headers,
            out_json = { 'message': '~last_name', 'error_code': 'INVALID_PARAMS'},
            status_code = 400
        )
        diff = exp.call(cfg)
        self.assertEqual({}, diff)

        
    ############################################################################
    #
    # /dogs/id PUT tests

    def test_dogs_update_successful(self):
        """
        The goal of the test is to verify that the /dogs end-point
        can update a dog when PUT and return the correct info.
        """
        cfg = Config()
        self.maxDiff = 32000

        in_headers = prepare_login_for_write_tests(cfg)

        in_dog = {
            "first_name": "Gambly",
            "last_name": "Husky",
        }

        out_dog = {
            "dog": {
                "id": 4,
                "first_name": "Gambly",
                "last_name": "Husky",
            }
        }

        exp = Expected(
            url = f'/dogs/4',
            method = Method.PUT,
            in_json = in_dog,
            in_headers = in_headers,
            out_json = out_dog,
            out_headers = { 'Location': f'{cfg.base_url}/dogs/4' },
            status_code = 200
        )
        diff = exp.call(cfg)
        self.assertEqual({}, diff)


    def test_dogs_update_successful_same_name(self):
        """
        The goal of the test is to verify that the /dogs end-point
        can update a dog even if the supplied names are unchanged
        when PUT and return the correct info.
        """
        cfg = Config()
        self.maxDiff = 32000

        in_headers = prepare_login_for_write_tests(cfg)

        in_dog = {
            "first_name": "Gambly",
            "last_name": "Husky",
        }

        out_dog = {
            "dog": {
                "id": 4,
                "first_name": "Gambly",
                "last_name": "Husky",
            }
        }

        exp = Expected(
            url = f'/dogs/4',
            method = Method.PUT,
            in_json = in_dog,
            in_headers = in_headers,
            out_json = out_dog,
            out_headers = { 'Location': f'{cfg.base_url}/dogs/4' },
            status_code = 200
        )
        diff = exp.call(cfg)
        self.assertEqual({}, diff)


    def test_dogs_update_create_fail_no_auth(self):
        """
        The goal of the test is to verify that the /dogs PUT end-point
        fails when the user is not logged in.
        """
        cfg = Config()
        self.maxDiff = 32000

        exp = Expected(
            url = '/dogs/4',
            method = Method.PUT,
            out_json = {
                'message': 'Invalid login.',
                'error_code': 'INVALID_CREDENTIAL',
            },
            status_code = 403
        )
        diff = exp.call(cfg)
        self.assertEqual({}, diff)


    def test_dogs_update_fail_no_first_name(self):
        """
        The goal of the test is to verify that the /dogs end-point
        fail to update a new dog when no first name was provided.
        """
        cfg = Config()
        self.maxDiff = 32000

        in_headers = prepare_login_for_write_tests(cfg)

        in_dog = {
            "first_name": "",
            "last_name": "Husky",
        }

        exp = Expected(
            url = f'/dogs/4',
            method = Method.PUT,
            in_json = in_dog,
            in_headers = in_headers,
            out_json = { 'message': '~first_name', 'error_code': 'INVALID_PARAMS'},
            status_code = 400
        )
        diff = exp.call(cfg)
        self.assertEqual({}, diff)


    def test_dogs_update_fail_no_last_name(self):
        """
        The goal of the test is to verify that the /dogs end-point
        fail to update a new dog when no last name was provided.
        """
        cfg = Config()
        self.maxDiff = 32000

        in_headers = prepare_login_for_write_tests(cfg)

        in_dog = {
            "first_name": "Gambly",
            "last_name": "",
        }

        exp = Expected(
            url = f'/dogs/4',
            method = Method.PUT,
            in_json = in_dog,
            in_headers = in_headers,
            out_json = { 'message': '~last_name', 'error_code': 'INVALID_PARAMS'},
            status_code = 400
        )
        diff = exp.call(cfg)
        self.assertEqual({}, diff)
        

    def test_dogs_update_fail_not_found(self):
        """
        The goal of the test is to verify that the /dogs end-point
        fail to update a non-existing dog.
        """
        cfg = Config()
        self.maxDiff = 32000

        in_headers = prepare_login_for_write_tests(cfg)

        in_dog = {
            "first_name": "Spotty",
            "last_name": "Tagado",
        }

        exp = Expected(
            url = f'/dogs/99',
            method = Method.PUT,
            in_json = in_dog,
            in_headers = in_headers,
            out_json = { 'message': 'Dog with id 99 does not exist.', 'error_code': 'OBJECT_NOT_FOUND'},
            status_code = 404
        )
        diff = exp.call(cfg)
        self.assertEqual({}, diff)
        

if __name__ == '__main__':
    unittest.main()

