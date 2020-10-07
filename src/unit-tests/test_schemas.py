import unittest
from unittest.mock import Mock, patch

from marshmallow.exceptions import ValidationError

import schemas
from util import ExpectedProblemException


class TestSchemas(unittest.TestCase):

    ############################################################################
    #
    # Dog

    def test_dump_Dog(self):
        """
        The goal of the test is to verify that the Dog schema
        serialize the expected data.
        """
        mock_data = {
            'id': 3,
            'first_name': 'fn',
            'last_name': 'ln',
        }

        expected_dump = {
            'id': 3,
            'first_name': 'fn',
            'last_name': 'ln',
        }

        data_dump = schemas.Dog().dump(mock_data)

        self.assertEqual(expected_dump, data_dump)


    def test_load_Dog(self):
        """
        The goal of the test is to verify that the Dog schema
        deserialize the expected data.
        """
        mock_data = {
            'first_name': 'fn',
            'last_name': 'ln',
        }

        expected_load = {
            'first_name': 'fn',
            'last_name': 'ln',
        }

        validated_data = schemas.Dog().load(mock_data)

        self.assertEqual(expected_load, validated_data)


    def test_load_Dog_fail_empty_first_name(self):
        """
        The goal of the test is to verify that the Dog schema
        raise an exception when the first name is empty.
        """
        mock_data = {
            'first_name': '',
            'last_name': 'ln',
        }

        with self.assertRaises(ValidationError) as raised:
            schemas.Dog().load(mock_data)

        self.assertIn('first_name', raised.exception.messages)


    def test_load_Dog_fail_empty_last_name(self):
        """
        The goal of the test is to verify that the Dog schema
        raise an exception when the last name is empty.
        """
        mock_data = {
            'first_name': 'fn',
            'last_name': '',
        }

        with self.assertRaises(ValidationError) as raised:
            schemas.Dog().load(mock_data)

        self.assertIn('last_name', raised.exception.messages)


    ############################################################################
    #
    # Login
    
    def test_load_Login(self):
        """
        The goal of the test is to verify that the Login schema
        deserialize the expected data.
        """
        mock_data = {
            'email': 'a@b.ca',
            'password': 'abcdef',
        }

        expected_load = {
            'email': 'a@b.ca',
            'cleartext_password': 'abcdef',
        }

        validated_data = schemas.Login().load(mock_data)

        self.assertEqual(expected_load, validated_data)


    def test_load_Login_fail_empty_email(self):
        """
        The goal of the test is to verify that the Login schema
        raise an exception when the email is empty.
        """
        mock_data = {
            'email': '',
            'password': 'abcdef',
        }

        with self.assertRaises(ValidationError) as raised:
            schemas.Login().load(mock_data)

        self.assertIn('email', raised.exception.messages)


    def test_load_Login_fail_empty_password(self):
        """
        The goal of the test is to verify that the Login schema
        raise an exception when the password is empty.
        """
        mock_data = {
            'email': 'a@b.ca',
            'password': '',
        }

        with self.assertRaises(ValidationError) as raised:
            schemas.Login().load(mock_data)

        self.assertIn('password', raised.exception.messages)


    ############################################################################
    #
    # House

    def test_dump_House(self):
        """
        The goal of the test is to verify that the House schema
        serialize the expected data.
        """
        mock_data = {
            'id': 3,
            'name': 'tt',
        }

        expected_dump = {
            'id': 3,
            'name': 'tt',
        }

        data_dump = schemas.House().dump(mock_data)

        self.assertEqual(expected_dump, data_dump)


    def test_load_House(self):
        """
        The goal of the test is to verify that the House schema
        deserialize the expected data.
        """
        mock_data = {
            'name': 'ttt',
        }

        expected_load = {
            'name': 'ttt',
        }

        validated_data = schemas.House().load(mock_data)

        self.assertEqual(expected_load, validated_data)


    def test_load_House_fail_empty_name(self):
        """
        The goal of the test is to verify that the House schema
        raise an exception when the name is empty.
        """
        mock_data = {
            'name': '',
        }

        with self.assertRaises(ValidationError) as raised:
            schemas.House().load(mock_data)

        self.assertIn('name', raised.exception.messages)


if __name__ == '__main__':
    unittest.main()

