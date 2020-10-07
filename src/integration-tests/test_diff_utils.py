import unittest
from unittest.mock import Mock, patch
import copy

import resto


class TestDiffSize(unittest.TestCase):
    """
    The goal of the tests are to verify that the _diff_size()
    returns the expected size for values, dicts and lists.
    """

    def test_diff_size_int(self):
        self.assertEqual(1, resto._diff_size(33))

    def test_diff_size_str(self):
        self.assertEqual(1, resto._diff_size('hello'))

    def test_diff_size_empty_dict(self):
        self.assertEqual(1, resto._diff_size({}))

    def test_diff_size_one_item_dict(self):
        self.assertEqual(2, resto._diff_size({'hello': 'world'}))

    def test_diff_size_two_items_dict(self):
        self.assertEqual(3, resto._diff_size({'hello': 'world', 'nice': 'day'}))

    def test_diff_size_empty_list(self):
        self.assertEqual(1, resto._diff_size([]))

    def test_diff_size_one_item_list(self):
        self.assertEqual(2, resto._diff_size(['hello']))

    def test_diff_size_five_items_list(self):
        self.assertEqual(5, resto._diff_size(['hello', 'world', 'nice', 'day']))

    def test_diff_size_dict_with_list(self):
        self.assertEqual(3, resto._diff_size({'hello': ['world']}))

    def test_diff_size_dict_with_longer_list(self):
        self.assertEqual(5, resto._diff_size({'hello': ['world', 'nice', 'day']}))

    def test_diff_size_empty_list_within_list(self):
        self.assertEqual(3, resto._diff_size([[[]]]))

    def test_diff_size_list_within_list(self):
        self.assertEqual(4, resto._diff_size([[['hello']]]))

    def test_diff_size_dict_within_list(self):
        self.assertEqual(4, resto._diff_size([{'hello': 'world', 'nice': 'day'}]))


class TestDiffLists(unittest.TestCase):
    """
    The goal of the test is to verify that the _diff_lists()
    returns the expected differences.
    (Remember, extra items in the received value are ignored.)
    """
    def test_diff_lists_empty_lists(self):
        self.assertEqual(([], 0), resto._diff_lists([], []))

    def test_diff_lists_empty_list_vs_one_item_list(self):
        self.assertEqual(([], 0), resto._diff_lists([], [2]))

    def test_diff_lists_identical_short_list(self):
        self.assertEqual(([], 0), resto._diff_lists([1], [1]))

    def test_diff_lists_identical_list_different_order(self):
        self.assertEqual(([], 0), resto._diff_lists([1, 2, 3], [2, 3, 1]))

    def test_diff_lists_empty_list_vs_none(self):
        self.assertEqual((None, 1), resto._diff_lists([], None) )

    def test_diff_lists_different_lists(self):
        self.assertEqual(([(1,2)], 2), resto._diff_lists([1], [2]))
        

class TestDiffDicts(unittest.TestCase):
    """
    The goal of the test is to verify that the _diff_dicts()
    returns the expected differences.
    (Remember, extra items in the received value are ignored.)
    """

    def test_diff_dicts_empty_dicts(self):
        self.assertEqual(({}, 0), resto._diff_dicts({}, {}))

    def test_diff_dicts_empty_dict_vs_filled_dict(self):
        self.assertEqual(({}, 0), resto._diff_dicts({}, {'a' : 'b'}))

    def test_diff_dicts_identical_dicts(self):
        self.assertEqual(({}, 0), resto._diff_dicts({'a': 'b', 'c': 'd'}, {'a': 'b', 'c': 'd'}))

    def test_diff_dicts_short_dict_vs_longer_dict(self):
        self.assertEqual(({}, 0), resto._diff_dicts({'a': 'b'}, {'a': 'b', 'c': 'd'}))

    def test_diff_dicts_empty_dict_vs_none(self):
        self.assertEqual((None, 1), resto._diff_dicts([], None) )

    def test_diff_dicts_short_dicts_containing_list(self):
        self.assertEqual(({}, 0), resto._diff_dicts({'a': [1, 2, 'b']}, {'a': [2, 'b', 1]}))

    def test_diff_dicts_deep_dict_diff(self):
        expected = {
            'a1': {
                'b1': {
                    'c1': {
                        'd1': 1,
                        'd2': 2,
                        'd3': 3,
                    },
                    'c2': [3, 4],
                },
                'b2': 4,
            },
            'a2': 'hello',
        }
        received = copy.deepcopy(expected)
        received['a1']['b1']['c1']['d1'] = 2 
        diff = { 'a1': { 'b1': { 'c1': { 'd1': (1, 2) }, }, }, }
        self.assertEqual((diff, 2), resto._diff_dicts(expected, received))


class TestDiffValues(unittest.TestCase):
    """
    The goal of the test is to verify that the _diff_values()
    returns the expected differences.
    (Remember, extra items in the received value are ignored.)
    """

    def test_diff_values_nones(self):
        self.assertEqual((None, 0), resto._diff_values(None, None))

    def test_diff_values_same_int(self):
        self.assertEqual((None, 0), resto._diff_values(1, 1))

    def test_diff_values_same_str(self):
        self.assertEqual((None, 0), resto._diff_values('hello', 'hello'))

    def test_diff_values_contains_str(self):
        self.assertEqual((None, 0), resto._diff_values('~hello', 'well, well, hello there!'))

    def test_diff_values_any_str(self):
        self.assertEqual((None, 0), resto._diff_values('*', 'well, well, hello there!'))

    def test_diff_values_same_lists(self):
        self.assertEqual(([], 0), resto._diff_values([1, 2], [1, 2]))

    def test_diff_values_same_dicts(self):
        self.assertEqual(({}, 0), resto._diff_values({'a': 'b'}, {'a': 'b'}))

    def test_diff_values_none_vs_int(self):
        self.assertEqual(((None, 1), 2), resto._diff_values(None, 1))

    def test_diff_values_different_int(self):
        self.assertEqual(((1, 2), 2), resto._diff_values(1, 2))

    def test_diff_values_different_str(self):
        self.assertEqual((('hello', 'bye'), 2), resto._diff_values('hello', 'bye'))

    def test_diff_values_different_lists(self):
        self.assertEqual((([(1, 7), (2, None)]), 3), resto._diff_values([1, 2], [7]))

    def test_diff_values_different_dicts(self):
        self.assertEqual(({'a': 'b'}, 1), resto._diff_values({'a' : 'b'}, {'c': 'd'}))


if __name__ == '__main__':
    unittest.main()

