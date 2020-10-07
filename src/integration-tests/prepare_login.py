from resto import Expected, Method, Config


############################################################################
#
# Authorization cache.
#
# Caching the authorization during test greatly speeds up testing as
# it avoids a round-trip to create the auth token.

_auth_cache = {}


def _get_auth_from_cache(user, password):
    """
    Retrieve a cached authentication token.
    Return None if not found.
    """
    global _auth_cache
    key = (user, password)
    if key in _auth_cache:
        return _auth_cache[key]
    return None


def _add_auth_to_cache(user, password, auth_token):
    """
    Add a cached authentication token.
    """
    global _auth_cache
    key = (user, password)
    _auth_cache[key] = auth_token


############################################################################
#
# External API.


def clear_auth_cache():
    """
    Clears the authentication cache.
    Used when the database users are changed incompatibly or when a test needs to test real logins.
    """
    global _auth_cache
    _auth_cache = {}
    

def prepare_login(cfg: Config, user=None, password=None) -> dict:
    """
    Login a user and return the necessary headers for authorization token.
    """
    if not user:
        user = "plat_o@example.com"
        
    if not password:
        password = "123456"

    auth_token = _get_auth_from_cache(user, password)
    if not auth_token:
        in_login = {
            "email": user,
            "password": password,
        }

        out_login = {
            'auth_token': '*',
        }

        exp = Expected(
            url = '/login',
            method = Method.POST,
            in_json = in_login,
            out_json = out_login,
            out_json_strict = False,
            status_code = 200
        )
        diff = exp.call(cfg)
        if diff:
            raise Exception(f'Authorization preparation failed.\nDifferences with expectations:\n{diff}')

        auth_token = exp.received_json['auth_token']
        _add_auth_to_cache(user, password, auth_token)

    auth_headers = { 'Authorization': f'Bearer {auth_token}' }

    return auth_headers


def prepare_login_for_read_tests(cfg: Config) -> dict:
    """
    Login a user that will always only be used for integration tests that solely read data.
    """
    return prepare_login(cfg, user='plat_o@example.com', password='123456')


def prepare_login_for_write_tests(cfg: Config) -> dict:
    """
    Login a user that will always be used for integration tests that modify data.
    """
    return prepare_login(cfg, user='salomon_deed@example.com', password='abcdef')


def prepare_login_for_write_user_tests(cfg: Config) -> dict:
    """
    Login a user that will always be used for integration tests that modify the logged-in user.
    """
    return prepare_login(cfg, user='aris_tottle@example.com', password='......')

