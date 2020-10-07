import datetime
import bcrypt
import jwt

from util import ExpectedProblemException, ErrorCode, extract_header_param


############################################################################
#
# Password hashing.


def hash_cleartext_password(cleartext_password: str) -> str:
    """
    Convert a clear-text password into a hashed password.
    Avoid keeping clear-text password in the DB!
    """
    salt = bcrypt.gensalt(rounds=12)
    # Note: bcrypt accepts only bytes-encoded text.
    encoded_password = cleartext_password.encode('utf8')
    return bcrypt.hashpw(encoded_password, salt).decode('utf8')


def verify_hashed_password(cleartext_password: str, hashed_password: str) -> bool:
    """
    Verify if the clear-text password corresponds to the given hashed password.
    """
    # Note: bcrypt accepts only bytes-encoded text.
    encoded_password = cleartext_password.encode('utf8')
    encoded_hash = hashed_password.encode('utf8')
    return bcrypt.checkpw(encoded_password, encoded_hash)


############################################################################
#
# JWT internal helpers.

# Normally, this auth secret would be in some environment variable and not in the code!
_dummy_auth_secret = "this is very easy to guess"

def _encode_payload(payload: dict) -> str:
    """
    Create a signed JWT token containing the given payload.
    """
    # Note: jwt.encode() returns bytes, we need to encode it into unicode text.
    # Normally, this auth secret would be in some environment variable and not in the code!
    global _dummy_auth_secret
    return jwt.encode(payload, _dummy_auth_secret, algorithm='HS256').decode('utf8')


def _decode_payload(token: str) -> dict:
    """
    Decode and verify a signed JWT token containing a payload.
    """
    # Normally, this auth secret would be in some environment variable and not in the code!
    global _dummy_auth_secret
    return jwt.decode(token, _dummy_auth_secret, algorithms=['HS256'])


############################################################################
#
# JWT generation and verification.


def encode_user_id_auth_token(user_id: int) -> str:
    """
    Create a signed JWT token containing the user id of the logged-in user.

    The token contains the following info ('claims' in JWT parlance):
        exp: the expiration date-time of the token. (This is a standard JWT claim.)
        now: sigh, the current time again, but with more precision...
        user_id: the user id.
    """
    # Note: we need to keep the current time twice because the 'exp' time is kept with only
    #       a second of precision, but when running tests, we can login multiple times
    #       per seconds... we need each token to be different!
    now = datetime.datetime.utcnow()
    expire = now + datetime.timedelta(minutes=60)
    return _encode_payload({
        'exp': expire,
        'now': str(now),
        'user_id': str(user_id),
    })


def _decode_user_id_auth_token(auth_token: str) -> int:
    """
    Decode the authentication token and extract the user id from it.
    Raises expected exception (util.ExpectedProblemException) when the token is invalid in any way.
    """
    try:
        payload = _decode_payload(auth_token)
        return int(payload['user_id'])
    except:
        # Note: for the front-end, we won't differentiate between bad tokens and expired tokens or other errors.
        raise ExpectedProblemException('Authentication expired. Please log in again.', error_code = ErrorCode.AUTH_TOKEN_EXPIRED, status_code=403)


def _validate_user_id_auth_token(auth_token: str) -> int:
    """
    Decode the authentication token and extract the user id from it.
    Normally, there would be revoked token handling, but this is just an dummy example.
    Raises expected exception (util.ExpectedProblemException) when the token is invalid in any way.
    """
    return _decode_user_id_auth_token(auth_token)


############################################################################
#
# JWT extraction and verification.


def _get_auth_token(event):
    """
    Extract the authorization token from the request event.
    Returns an empty token on error.
    """
    auth_header = extract_header_param(event, 'Authorization')
    if not auth_header:
        return None

    auth_header_parts = auth_header.split()
    if not auth_header_parts or len(auth_header_parts) != 2:
        return None

    return auth_header_parts[1]


def validate_user_id_auth_token(event) -> int:
    """
    Extract the authentication token, decode it and extract the user id from it.
    Raises expected exception (util.ExpectedProblemException) when the token is invalid in any way.
    """
    auth_token = _get_auth_token(event)
    if not auth_token:
        raise ExpectedProblemException('Invalid login.', error_code = ErrorCode.INVALID_CREDENTIAL, status_code=403)

    return _validate_user_id_auth_token(auth_token)

