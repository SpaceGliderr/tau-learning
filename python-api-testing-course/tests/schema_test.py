import json
from utils.config import BASE_URI
import requests
from cerberus import Validator
from assertpy.assertpy import assert_that, soft_assertions


schema = {
    "fname": {"type": "string"},
    "lname": {"type": "string"},
    "person_id": {"type": "integer"},
    "timestamp": {"type": "string"},
}


def test_read_one_operation_has_expected_schema():
    response = requests.get(f"{BASE_URI}/1")
    person = json.loads(response.text)

    # require_all to True is global flag that specifies all keys in response is required
    # If specific key level, add at the schema dict "fname": {"type": "string", "required": True}
    validator = Validator(schema, require_all=True)
    is_valid = validator.validate(person)  # Validate the Python object

    assert_that(is_valid, description=validator.errors).is_true()


def test_read_all_operation_has_expected_schema():
    response = requests.get(f"{BASE_URI}")
    persons = json.loads(response.text)

    validator = Validator(schema, require_all=True)

    with soft_assertions():
        for person in persons:
            is_valid = validator.validate(person)
            assert_that(is_valid, description=validator.errors).is_true()
