import unittest
from unittest.mock import Mock, patch

import  util


class TestUtilExtractEvent(unittest.TestCase):


    def test_extract_event_param(self):
        """
        The goal of the test is to verify that extract_event_param()
        extracts parameters correctly in all cases.
        """
        empty = {}

        self.assertEqual(None, util.extract_event_param(empty, ''))
        self.assertEqual(None, util.extract_event_param(empty, 'non-existing'))
        self.assertEqual(None, util.extract_event_param(empty, 'non-existing/param'))

        self.assertEqual(1, util.extract_event_param(empty, '', default=1))
        self.assertEqual(2, util.extract_event_param(empty, 'non-existing', default=2))
        self.assertEqual(3, util.extract_event_param(empty, 'non-existing/param', default=3))

        simple = { 'key': 'value' }

        self.assertEqual(None, util.extract_event_param(simple, ''))
        self.assertEqual(None, util.extract_event_param(simple, 'non-existing'))
        self.assertEqual(None, util.extract_event_param(simple, 'non-existing/param'))
        self.assertEqual('value', util.extract_event_param(simple, 'key'))
        self.assertEqual(None, util.extract_event_param(simple, 'key/oops'))

        self.assertEqual(1, util.extract_event_param(simple, '', default=1))
        self.assertEqual(2, util.extract_event_param(simple, 'non-existing', default=2))
        self.assertEqual(3, util.extract_event_param(simple, 'non-existing/param', default=3))
        self.assertEqual(4, util.extract_event_param(simple, 'key/oops', default=4))
        self.assertEqual('value', util.extract_event_param(simple, 'key', default=5))

        complex = { 'key1': { 'key2': 'value' } }

        self.assertEqual(None, util.extract_event_param(complex, ''))
        self.assertEqual(None, util.extract_event_param(complex, 'non-existing'))
        self.assertEqual(None, util.extract_event_param(complex, 'non-existing/param'))
        self.assertEqual({ 'key2': 'value' }, util.extract_event_param(complex, 'key1'))
        self.assertEqual(None, util.extract_event_param(complex, 'key1/oops'))
        self.assertEqual('value', util.extract_event_param(complex, 'key1/key2'))
        self.assertEqual(None, util.extract_event_param(complex, 'key1/key2/oops'))

        self.assertEqual(1, util.extract_event_param(complex, '', default=1))
        self.assertEqual(2, util.extract_event_param(complex, 'non-existing', default=2))
        self.assertEqual(3, util.extract_event_param(complex, 'non-existing/param', default=3))
        self.assertEqual(4, util.extract_event_param(complex, 'key1/oops', default=4))
        self.assertEqual(5, util.extract_event_param(complex, 'key1/key2/oops', default=5))
        self.assertEqual('value', util.extract_event_param(complex, 'key1/key2', default=6))


    def test_extract_url_param(self):
        """
        The goal of the test is to verify that extract_url_param()
        extracts parameters correctly in all cases.
        """
        empty = {}

        self.assertEqual(None, util.extract_url_param(empty, ''))
        self.assertEqual(None, util.extract_url_param(empty, 'non-existing'))

        self.assertEqual(1, util.extract_url_param(empty, '', default=1))
        self.assertEqual(2, util.extract_url_param(empty, 'non-existing', default=2))

        event = { 'queryStringParameters': { 'key': 'value' } }

        self.assertEqual(None, util.extract_url_param(event, ''))
        self.assertEqual(None, util.extract_url_param(event, 'non-existing'))
        self.assertEqual('value', util.extract_url_param(event, 'key'))

        self.assertEqual(1, util.extract_url_param(event, '', default=1))
        self.assertEqual(2, util.extract_url_param(event, 'non-existing', default=2))
        self.assertEqual('value', util.extract_url_param(event, 'key', default=3))


    def test_extract_path_param(self):
        """
        The goal of the test is to verify that extract_path_param()
        extracts parameters correctly in all cases.
        """
        empty = {}

        self.assertEqual(None, util.extract_path_param(empty, ''))
        self.assertEqual(None, util.extract_path_param(empty, 'non-existing'))

        self.assertEqual(1, util.extract_path_param(empty, '', default=1))
        self.assertEqual(2, util.extract_path_param(empty, 'non-existing', default=2))

        event = { 'pathParameters': { 'key': 'value' } }

        self.assertEqual(None, util.extract_path_param(event, ''))
        self.assertEqual(None, util.extract_path_param(event, 'non-existing'))
        self.assertEqual('value', util.extract_path_param(event, 'key'))

        self.assertEqual(1, util.extract_path_param(event, '', default=1))
        self.assertEqual(2, util.extract_path_param(event, 'non-existing', default=2))
        self.assertEqual('value', util.extract_path_param(event, 'key', default=3))


    def test_extract_header_param(self):
        """
        The goal of the test is to verify that extract_header_param()
        extracts parameters correctly in all cases.
        """
        empty = {}

        self.assertEqual(None, util.extract_header_param(empty, ''))
        self.assertEqual(None, util.extract_header_param(empty, 'non-existing'))

        self.assertEqual(1, util.extract_header_param(empty, '', default=1))
        self.assertEqual(2, util.extract_header_param(empty, 'non-existing', default=2))

        event = { 'headers': { 'key': 'value' } }

        self.assertEqual(None, util.extract_header_param(event, ''))
        self.assertEqual(None, util.extract_header_param(event, 'non-existing'))
        self.assertEqual('value', util.extract_header_param(event, 'key'))

        self.assertEqual(1, util.extract_header_param(event, '', default=1))
        self.assertEqual(2, util.extract_header_param(event, 'non-existing', default=2))
        self.assertEqual('value', util.extract_header_param(event, 'key', default=3))


if __name__ == '__main__':
    unittest.main()

