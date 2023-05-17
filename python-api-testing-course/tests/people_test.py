import json
import uuid
from assertpy.assertpy import assert_that, soft_assertions

import requests

from utils.config import BASE_URI


def create_new_unique_user():
    unique_last_name = f"User {str(uuid.uuid4())}"

    payload = json.dumps({
        "fname": "New",
        "lname": unique_last_name
    })

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    response = requests.post(url=BASE_URI, data=payload, headers=headers)

    return response, unique_last_name


def get_all_users():
    response = requests.get(BASE_URI)
    peoples = response.json()

    return response, peoples


def test_read_all_has_kent():
    # Make a GET HTTP request to people API endpoint
    response = requests.get(BASE_URI) # Good idea to isolate config from tests
    # Use the json method to convert JSON string into dict
    response_text = response.json()

    print(response_text)

    # Assert using assertpy library2
    assert_that(response.status_code).is_equal_to(200)
    first_names = [people["fname"] for people in response_text]
    assert_that(first_names).contains("Kent")


def test_new_person_can_be_added():
    response, unique_last_name = create_new_unique_user()
    
    peoples = requests.get(BASE_URI).json()
    is_new_user_created = list(filter(lambda person: person["lname"] == unique_last_name, peoples))

    print(is_new_user_created)

    assert_that(response.status_code).is_equal_to(204)
    assert_that(is_new_user_created).is_not_empty()


def test_person_can_be_deleted():
    response, unique_last_name = create_new_unique_user()
    _, all_users = get_all_users()

    user_to_delete = list(filter(lambda person: person["lname"] == unique_last_name, all_users))[0]

    print(user_to_delete["person_id"])

    response = requests.delete(f"{BASE_URI}/{user_to_delete['person_id']}")
    
    print(response.text)
    print(response.headers)

    assert_that(response.status_code).is_equal_to(200)

    # _, all_users = get_all_users()
    # user_to_delete = list(filter(lambda person: person["lname"] == unique_last_name, all_users))

    # assert_that(user_to_delete).is_empty()


def test_person_can_be_updated():
    response, unique_last_name = create_new_unique_user()
    _, all_users = get_all_users()

    user_to_update = list(filter(lambda person: person["lname"] == unique_last_name, all_users))[0]

    new_unique_first_name = f"Updated {str(uuid.uuid4())}"
    new_unique_last_name = f"User {str(uuid.uuid4())}"

    update_payload = json.dumps({
        "fname": new_unique_first_name,
        "lname": new_unique_last_name
    })

    headers = headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    response = requests.put(url=f"{BASE_URI}/{user_to_update['person_id']}", data=update_payload, headers=headers)

    assert_that(response.status_code).is_equal_to(requests.codes.ok)
    assert_that(response.json()["fname"]).is_equal_to(new_unique_first_name)
    assert_that(response.json()["lname"]).is_equal_to(new_unique_last_name)


def test_read_all_has_kent_using_extracting():
    # Make a GET HTTP request to people API endpoint
    response = requests.get(BASE_URI) # Good idea to isolate config from tests
    # Use the json method to convert JSON string into dict
    response_text = response.json()

    # Assert using assertpy library2
    assert_that(response.status_code).is_equal_to(200)
    assert_that(response_text).extracting("fname").contains("Kent").is_not_empty()


def test_read_all_has_kent_with_soft_assertion():
    response = requests.get(BASE_URI) # Good idea to isolate config from tests

    with soft_assertions():
        assert_that(response.status_code).is_equal_to(204)
        # Use the json method to convert JSON string into dict
        response_text = response.json()
        assert_that(response_text).extracting("fname").contains("zsakljdbfsda").is_not_empty()
