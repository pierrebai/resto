import auth
import schemas
import util


@util.catch_exceptions
def dogs_handler(event, context):
    """
    Dispatch to the correct sub-handler depending if it is a GET or POST.
    """
    return util.dispatch_to_http_handler(
        event, context,
        get_handler=_dogs_get_handler,
        post_handler=_dogs_post_handler,
        put_handler=_dogs_put_handler)


############################################################################
#
# DB emulation

_next_dog_id = 1

class Dog:
    def __init__(self, first_name, last_name):
        global _next_dog_id
        self.id = _next_dog_id
        self.first_name = first_name
        self.last_name = last_name
        _next_dog_id += 1


_db_dogs = [
    Dog("Blacky", "Doggy"),
    Dog("Prancer", "Labrador"),
    Dog("Fluffy", "Hair"),
]


def _get_dogs_from_db():
    global _db_dogs
    return _db_dogs


def _add_dog_to_db(dog):
    global _db_dogs
    return _db_dogs.append(dog)


def _find_dog(id: int):
    """
    Find the dog with the given id.
    Return that instance if it exists, else raise an ExpectedProblemException
    with error code OBJECT_NOT_FOUND.
    """
    global _db_dogs
    for h in _db_dogs:
        if h.id == id:
            return h
    raise util.ExpectedProblemException(f'Dog with id {id} does not exist.', util.ErrorCode.OBJECT_NOT_FOUND, status_code=404)


############################################################################
#
# /dogs GET


def _dogs_get_handler(event, context):
    """
    Retrieve all dogs.
    Return the dog information: name etc. See: schemas.Dog.
    """
    user_id = auth.validate_user_id_auth_token(event)
    
    dog_schema = schemas.Dog()

    id = util.extract_path_param(event, 'id')
    if id is None:
        dogs = _get_dogs_from_db()
        result = { 'total_item_count': len(dogs) }
        result['dogs'] = [dog_schema.dump(d) for d in dogs]
    else:
        dog = _find_dog(int(id))
        result = { 'dog': dog_schema.dump(dog) }

    return util.return_success_body(result)


############################################################################
#
# /dogs POST


def _dogs_post_handler(event, context):
    """
    Create a new dog. See: schemas.CreateDog.
    Return all information about the new dog. See: schemas.Dog.
    """
    user_id = auth.validate_user_id_auth_token(event)

    dog_schema = schemas.Dog()

    params = util.unmarshall_json_body_params(event, dog_schema)

    new_dog = Dog(params["first_name"], params["last_name"])

    _add_dog_to_db(new_dog)

    location = f'/dogs/{new_dog.id}'
    result = { "dog" : schemas.Dog().dump(new_dog) }

    return util.return_success_body_with_location(result, location)


############################################################################
#
# /dogs/{id} PUT


def _dogs_put_handler(event, context):
    """
    Update an existing dog. See: schemas.UpdateDog.
    Return all information about the dog. See: schemas.Dog.
    """
    user_id = auth.validate_user_id_auth_token(event)

    dog_schema = schemas.Dog()
    params = util.unmarshall_json_body_params(event, dog_schema)

    id = util.extract_path_param(event, 'id')
    
    dog_to_update = _find_dog(int(id))

    dog_to_update.first_name = params["first_name"]
    dog_to_update.last_name = params["last_name"]

    location = f'/dogs/{dog_to_update.id}'
    result = { "dog" : dog_schema.dump(dog_to_update) }

    return util.return_success_body_with_location(result, location, status_code=200)
