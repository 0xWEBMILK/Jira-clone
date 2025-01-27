import pytest
import re


from jira_clone.app.auth.hashing import JWTHasher

from jira_clone.app.schemas.schemas import (ColorsEnum,
                                            UserSchema,
                                            TagSchema,
                                            CategorySchema,
                                            TaskSchema)


# User
def test_user_encode():
    test_user = UserSchema(
        first_name='John',
        last_name='Doe',

        username="super_username",
        password="super_password",
        email="superemail@superdomain.zone",
    )

    jwt_hasher = JWTHasher(key='super_key', alg='HS256')

    encoded = jwt_hasher.encode(test_user)

    assert re.fullmatch(r"^[A-Za-z0-9-_]+(.[A-Za-z0-9-_]+){2}$", encoded)

def test_user_decode():
    test_user = UserSchema(
        first_name='John',
        last_name='Doe',

        username="super_username",
        password="super_password",
        email="superemail@superdomain.zone",
    )

    jwt_hasher = JWTHasher(key='super_key', alg='HS256')

    encoded = jwt_hasher.encode(test_user)
    decoded = UserSchema(**jwt_hasher.decode(encoded))

    assert decoded == test_user


def test_task_encode():
    test_task = TaskSchema(
        title="Test Task Title",
        description="Test Description",

        creator="John Doe",
        performers=["Test Performer One", "Test Performer Two"],
        tags=["Test Tag One", "Test Tag Two"],
    )

    jwt_hasher = JWTHasher(key='super_key', alg='HS256')

    encoded = jwt_hasher.encode(test_task)

    assert re.fullmatch(r"^[A-Za-z0-9-_]+(.[A-Za-z0-9-_]+){2}$", encoded)

def test_task_decode():
    test_task = TaskSchema(
        title="Test Task Title",
        description="Test Description",

        creator="John Doe",
        performers=["Test Performer One", "Test Performer Two"],
        tags=["Test Tag One", "Test Tag Two"],
    )

    jwt_hasher = JWTHasher(key='super_key', alg='HS256')

    encoded = jwt_hasher.encode(test_task)
    decoded = TaskSchema(**jwt_hasher.decode(encoded))

    assert decoded == test_task

def test_tag_encode():
    test_tag = TagSchema(
        name="Test Tag Title",
        color=ColorsEnum.RED
    )

    jwt_hasher = JWTHasher(key='super_key', alg='HS256')

    encoded = jwt_hasher.encode(test_tag)

    assert re.fullmatch(r"^[A-Za-z0-9-_]+(.[A-Za-z0-9-_]+){2}$", encoded)

def test_tag_decode():
    test_tag = TagSchema(
        name="Test Tag Title",
        color=ColorsEnum.RED
    )

    jwt_hasher = JWTHasher(key='super_key', alg='HS256')

    encoded = jwt_hasher.encode(test_tag)
    decoded = TagSchema(**jwt_hasher.decode(encoded))

    assert decoded == test_tag

def test_category_encode():
    test_category = CategorySchema(
        name="Test Category Title",
        color=ColorsEnum.RED
    )

    jwt_hasher = JWTHasher(key='super_key', alg='HS256')

    encoded = jwt_hasher.encode(test_category)

    assert re.fullmatch(r"^[A-Za-z0-9-_]+(.[A-Za-z0-9-_]+){2}$", encoded)

def test_category_decode():
    test_category = CategorySchema(
        name="Test Category Title",
        color=ColorsEnum.RED
    )

    jwt_hasher = JWTHasher(key='super_key', alg='HS256')

    encoded = jwt_hasher.encode(test_category)
    decoded = CategorySchema(**jwt_hasher.decode(encoded))

    assert decoded == test_category