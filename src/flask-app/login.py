import datetime

import schemas
import util
import auth


@util.catch_exceptions
def login_handler(event, context):
    """
    Handle the /login POST request.
    """
    params = util.unmarshall_json_body_params(event, schemas.Login())

    email = params["email"]

    # Here we would normally verify the hashed password...
    # For our example, we don't have a user database with hashed password...
    known_users = {
        'plat_o@example.com' : '123456',
        'salomon_deed@example.com' : 'abcdef',
        'aris_tottle@example.com': '......',
    }

    if email not in known_users:
        return util.return_error('Invalid login.', util.ErrorCode.INVALID_CREDENTIAL, status_code = 403)

    cleartext_password = params['cleartext_password']
    if cleartext_password != known_users[email]:
        return util.return_error('Invalid login.', util.ErrorCode.INVALID_CREDENTIAL, status_code = 403)

    # For this example we create a dummy user id based on the email.
    # Normally it would come from a database.
    user_id = email.__hash__()

    auth_token = auth.encode_user_id_auth_token(user_id)

    result = {
        'auth_token': auth_token
    }

    return util.return_success_body(result)


@util.catch_exceptions
def logout_handler(event, context):
    """
    Handle the /logout POST request.
    """
    user_id = auth.validate_user_id_auth_token(event)

    # We will pretend the user is logged out...

    result = { 'message': 'Logout successful.' }
    
    return util.return_success_body(result)


@util.catch_exceptions
def refresh_token_handler(event, context):
    """
    Handle the /refresh_token GET request.
    """
    user_id = auth.validate_user_id_auth_token(event)

    auth_token = auth.encode_user_id_auth_token(user_id, org_id)

    result = { 'auth_token': auth_token }

    return util.return_success_body(result)

