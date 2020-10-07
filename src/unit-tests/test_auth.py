import unittest
from unittest.mock import Mock, patch

import os

import auth
from util import ExpectedProblemException


class TestAuth(unittest.TestCase):

    def test_password_hashing(self):
        """
        The goal of the test is to verify that hash_cleartext_password()
        and verify_hashed_password work correctly.
        """
        cleartext = 'summer tale'
        hashed = auth.hash_cleartext_password(cleartext)

        self.assertTrue(isinstance(hashed, str))
        self.assertNotEqual(cleartext, hashed)
        self.assertTrue(auth.verify_hashed_password(cleartext, hashed))


    def test_user_id_token(self):
        """
        The goal of the test is to verify that encode_user_id_auth_token()
        creates a valid token that can be decoded with _decode_user_id_auth_token().
        """
        token = auth.encode_user_id_auth_token(33)
        self.assertTrue(isinstance(token, str))

        self.assertEqual((33), auth._decode_user_id_auth_token(token))


    def test_invalid_user_id_token(self):
        """
        The goal of the test is to verify that _decode_user_id_auth_token()
        raises an exception when the token is invalid.
        """
        def bad_decode():
            token = 'abcdef'
            auth._decode_user_id_auth_token(token)

        self.assertRaises(ExpectedProblemException, bad_decode)


if __name__ == '__main__':
    unittest.main()

