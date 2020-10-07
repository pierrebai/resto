import auth
import schemas
import util


@util.catch_exceptions
def houses_handler(event, context):
    """
    Dispatch to the correct sub-handler depending if it is a GET or POST.
    """
    return util.dispatch_to_http_handler(
        event, context,
        get_handler = _houses_get_handler,
        post_handler = _houses_post_handler,
        put_handler = _houses_put_handler,
        delete_handler = _houses_delete_handler)


############################################################################
#
# DB emulation

_next_house_id = 1

class House:
    def __init__(self, name):
        global _next_house_id
        self.id = _next_house_id
        self.name = name
        _next_house_id += 1


_db_houses = [
    House("Frank's house"),
    House("Janet's house"),
    House("Marcy's house"),
]


def _get_houses_from_db():
    global _db_houses
    return _db_houses


def _add_house_to_db(house):
    global _db_houses
    return _db_houses.append(house)


def _delete_house_from_db(house):
    global _db_houses
    return _db_houses.remove(house)


def _find_house(id: int):
    """
    Find the house with the given id.
    Return that instance if it exists, else raise an ExpectedProblemException
    with error code OBJECT_NOT_FOUND.
    """
    global _db_houses
    for h in _db_houses:
        if h.id == id:
            return h
    raise util.ExpectedProblemException(f'House with id {id} does not exist.', util.ErrorCode.OBJECT_NOT_FOUND, status_code=404)


############################################################################
#
# /houses GET


def _houses_get_handler(event, context):
    """
    Retrieve all houses or a given house.
    Return the house information. See: schemas.House.
    """
    user_id = auth.validate_user_id_auth_token(event)

    house_schema = schemas.House()

    id = util.extract_path_param(event, 'id')
    if id is None:
        houses = _get_houses_from_db()
        result = { 'total_item_count': len(houses) }
        result['houses'] = [house_schema.dump(h) for h in houses]
    else:
        house = _find_house(int(id))
        result = { 'house': house_schema.dump(house) }

    return util.return_success_body(result)


############################################################################
#
# /houses POST


def _houses_post_handler(event, context):
    """
    Create a new house.
    Return all information about the new houses. See: schemas.House.
    """
    user_id = auth.validate_user_id_auth_token(event)

    house_schema = schemas.House()

    params = util.unmarshall_json_body_params(event, house_schema)

    name = params["name"]

    new_house = House(name)
    _add_house_to_db(new_house)
    
    location = f'/houses/{new_house.id}'
    result = { "house" : house_schema.dump(new_house) }

    return util.return_success_body_with_location(result, location)


############################################################################
#
# /houses/{id} PUT


def _houses_put_handler(event, context):
    """
    Update an existing house. See: schemas.House.
    Return all information about the house. See: schemas.House.
    """
    user_id = auth.validate_user_id_auth_token(event)

    id = util.extract_path_param(event, 'id')

    house_schema = schemas.House()

    params = util.unmarshall_json_body_params(event, house_schema)

    name = params["name"]

    house_to_update = _find_house(int(id))
    house_to_update.name = name

    location = f'/houses/{house_to_update.id}'
    result = { "house" : house_schema.dump(house_to_update) }

    return util.return_success_body_with_location(result, location, status_code=200)


############################################################################
#
# /houses/{id} DELETE


def _houses_delete_handler(event, context):
    """
    Delete an existing house.
    """
    user_id = auth.validate_user_id_auth_token(event)

    id = util.extract_path_param(event, 'id')

    house_to_delete = _find_house(int(id))

    _delete_house_from_db(house_to_delete)

    result = { 'message': f'House {id} deletion successful.' }
    
    return util.return_success_body(result)


