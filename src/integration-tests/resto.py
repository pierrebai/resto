import requests
import json
import enum
import os


############################################################################
#
# Configuration


def _get_config(name, default=None):
    """Get an configuration value, with a default if the configuration is not set."""
    return os.getenv(name, default)


class Config():
    """
    Configuration class for the resto module.

    Configurable parameters:
      - base_url: the base URL from which all other are relative.
                  defaults to http://localhost:3000
    """
    def __init__(self, base_url: str = None):
        if not base_url:
            base_url = _get_config('BACKENDURL', 'http://localhost:3000')
        self.base_url = base_url

    def build_full_url(self, url: str) -> str:
        full_url = self.base_url + url
        return full_url


############################################################################
#
# Expected responses


_requests_session = None
def _get_session() -> requests.Session:
    global _requests_session
    if not _requests_session:
        _requests_session = requests.Session()
    return _requests_session


class Method(enum.Enum):
    GET = 1
    POST = 2
    PUT = 3
    DELETE = 4


class Expected():
    """
    Describe the expected response to a REST request.
    """
    def __init__(
            self,
            url: str = '',
            method: Method = Method.GET,
            params: dict = None,
            in_headers: dict = None,
            out_headers: dict = None,
            in_json: dict = None,
            out_json: dict = None,
            out_json_strict: bool = True,
            status_code: int = 200,
            **kwargs):
        self.method = method
        self.url = url
        self.params = params
        self.in_headers = in_headers
        self.out_headers = out_headers
        self.in_json = in_json
        self.out_json = out_json
        self.out_json_strict = out_json_strict
        self.status_code = status_code

        self.received_headers = {}
        self.received_json = {}
        self.received_code = 0

        for k, v in kwargs.items():
            setattr(self, k, v)

    def call(self, config: Config) -> dict:
        """
        Call the rest API. Return the diff with the expected status code, JSON and headers.
        """
        full_url = config.build_full_url(self.url)

        session = _get_session()

        methods = {
            Method.GET: session.get,
            Method.POST: session.post,
            Method.PUT: session.put,
            Method.DELETE: session.delete,
        }
        meth = methods[self.method]
        
        with meth(full_url, params=self.params, headers=self.in_headers, json=self.in_json, stream=False) as response:
            diff = {}

            try:
                self.received_json = response.json()
            except:
                self.received_json = {}
            self.received_headers = response.headers
            self.received_code = response.status_code

            diff.update(self.diff_json(self.received_json))
            diff.update(self.diff_headers(self.received_headers))

            if self.received_code != self.status_code:
                diff['status_code'] = (self.status_code, self.received_code)

        return diff

    def diff_json(self, received_json: dict ) -> dict:
        """
        Compare the received JSON to the expected one.
        Return a dictionary of differing items.
        """
        if received_json is None:
            return {} if self.out_json is None else dict(self.out_json)
        
        if self.out_json is None:
            if self.out_json_strict:
                return dict(received_json)
            else:
                return {}

        diff = {}

        if self.out_json_strict:
            rev_diff, _ = _diff_dicts(received_json, self.out_json)
            diff.update(rev_diff)
        
        expected_diff, _ = _diff_dicts(self.out_json, received_json)
        diff.update(expected_diff)
        
        return diff

    def diff_headers(self, received_headers: dict) -> dict:
        """
        Compare the received headers to the expected ones.
        Return a dictionary of differing items.
        """
        if not received_headers:
            return {} if not self.out_headers else dict(self.out_headers)
        
        if not self.out_headers:
            return {}

        diff, _ = _diff_dicts(_lowercase_keys(self.out_headers), _lowercase_keys(received_headers))
        
        return diff


############################################################################
#
# JSON diff helpers


def _diff_values(expected, received) -> (object, int):
    """
    Compare an expected value with a received one.
    Return a pair containing the difference between the values and the size of the difference.
    """
    if type(expected) is dict:
        if type(received) is dict:
            return _diff_dicts(expected, received)
        sub_diff = received
    elif type(expected) is list:
        if type(received) is list: 
            return _diff_lists(expected, received)
        sub_diff = received
    elif type(expected) is str:
        if type(received) is str:
            return _diff_str(expected, received)
        sub_diff = (expected, received)
    elif expected != received:
        sub_diff = (expected, received)
    else:
        return (None, 0)

    return (sub_diff, _diff_size(received) + _diff_size(expected))


def _diff_str(expected: str, received: str) -> (object, int):
    """
    Compare an expected text with a received one.

    If the expected text starts with '~', then the rest of the text only
    needs to be contained in the received text.

    If the expected text is '*', then it matches anything, including an empty text.

    Return a pair containing the difference between the values and the size of the difference.
    For text we return both texts if they differ, else None. The size is always 2 when they differ.
    """
    if expected.startswith('~'):
        matches = (expected[1:] in received)
    elif received.startswith('~'):
        matches = (received[1:] in expected)
    elif expected == '*' or received == '*':
        matches = True
    else:
        matches = (expected == received)
    
    if matches:
        return (None, 0)
    else:
        return ((expected, received), 2)


def _lowercase_keys(in_dict: dict) -> dict:
    """
    Create a new dict but with all string keys converted to lower-case.
    """
    lc_dict = {}
    for k, v in in_dict.items():
        if type(k) is str:
            k = k.lower()
        lc_dict[k] = k
    return lc_dict


def _diff_dicts(expected: dict, received: dict) -> (dict, int):
    """
    Compare an expected dictionary with a received one.
    The extra keys in the received one are ignored.
    Return a pair containing the difference between the dicts and the size of the difference.
    """
    diff = {}
    size = 0

    # Protect against None
    if received is None:
        return (None, 1)

    for k, v in expected.items():
        if k not in received:
            diff[k] = v
            size += _diff_size(v)
        else:
            rv = received[k]
            sub_diff, sub_size = _diff_values(v, rv)
            if sub_diff:
                diff[k] = sub_diff
                size += sub_size

    return (diff, size)

def _diff_size(value) -> int:
    """
    Calculate the size of an value.
    It's the recursive size of all containers.
    The existence of the value itself is always counted as one, so for example empty list have size 1.
    """
    size = 1

    if type(value) is dict:
        for k, v in value.items():
            size += _diff_size(v)
    elif type(value) is list:
        for v in value:
            size += _diff_size(v)

    return size


def _diff_lists(expected: list, received: list) -> list:
    """
    Compare an expected list with a received one.
    The extra items in the received one are ignored.
    Return a pair containing the difference between the lists and the size of the difference.
    """
    diff = []
    size = 0

    # Protect from being passed None
    if received is None:
        return (None, 1)

    # We will be tracking each item that is already matched.
    expected_matched = [False for e in expected]
    received_matched = [False for r in received]

    # First, we do perfect matches, keeping track of best matches.
    # For each item, we keep a list of tuples (best match size, best match index)
    # Perfect matches will be recorded in the _matched list above.
    expected_matches = [[] for e in expected]
    for ei in range(0, len(expected)):
        v = expected[ei]
        for ri in range(0, len(received)):
            # Verify if the received item has already been perfectly matched.
            if received_matched[ri]:
                continue

            # Try to perfectly match the expected and received item.
            # If we find a perfect match, keep only that match in the list of matches.
            rv = received[ri]
            sub_diff, sub_size = _diff_values(v, rv)
            if not sub_diff:
                received_matched[ri] = True
                expected_matched[ei] = True
                expected_matches[ei] = [(0, ri)]
                break

            # Record the imperfect match size.
            expected_matches[ei].append((sub_size, ri))

    # Now, we do imperfect matches.

    # Sort all matches in order of difference sizes.
    best_matches = []
    for ei in range(0, len(expected)):
        matches = expected_matches[ei]
        for match in matches:
            best_matches.append((match[0], ei, match[1]))
    best_matches.sort()

    # In the best match order, compare the expected value and its best-matching received value.
    # Only use each value once.
    for bm in best_matches:
        ei = bm[1]
        if expected_matched[ei]:
            continue

        ri = bm[2]
        if received_matched[ri]:
            continue

        v = expected[ei]
        rv = received[ri]

        sub_diff, sub_size = _diff_values(v, rv)
        diff.append(sub_diff)
        size += sub_size

        expected_matched[ei] = True
        received_matched[ri] = True

    # If there were fewer received values than expected,
    # pair the unmatched expected with None
    for ei in range(0, len(expected)):
        if not expected_matched[ei]:
            diff.append((expected[ei], None))
            size += 1

    return (diff, size)


############################################################################
#
# Run as a program. TODO


def _main():
    pass


if __name__ == '__main__':
    _main()

