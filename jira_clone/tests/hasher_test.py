import pytest
import re


from jira_clone.app.auth.hashing import HasherInterface, JWTHasher
from jira_clone.app.models.models import User, Task

# User
def test_user_encode():
    test_user = User(
        first_name='John',
        last_name='Doe',

        username="super_username",
        password="super_password",
        email="superemail@superdomain.zone",
    )

    jwt_hasher = JWTHasher(key='super_key', alg='HS256')
    jwt_hasher_interface = HasherInterface(jwt_hasher)

    encoded = jwt_hasher_interface.encode(test_user)

    assert re.fullmatch(r"^[A-Za-z0-9-_]+(.[A-Za-z0-9-_]+){2}$", encoded)

def test_user_decode():
    test_user = User(
        first_name='John',
        last_name='Doe',

        username="super_username",
        password="super_password",
        email="superemail@superdomain.zone",
    )

    jwt_hasher = JWTHasher(key='super_key', alg='HS256')
    jwt_hasher_interface = HasherInterface(jwt_hasher)

    encoded = jwt_hasher_interface.encode(test_user)
    decoded = User(**jwt_hasher_interface.decode(encoded))

    assert decoded == test_user

# Task
def test_task_encode():
    test_task = Task(
        title="Test Task Title",
        description="Test Description",

        creator="John Doe",
        performers=["Test Performer One", "Test Performer Two"],
        tags=["Test Tag One", "Test Tag Two"],
    )

    jwt_hasher = JWTHasher(key='super_key', alg='HS256')
    jwt_hasher_interface = HasherInterface(jwt_hasher)

    encoded = jwt_hasher_interface.encode(test_task)

    assert re.fullmatch(r"^[A-Za-z0-9-_]+(.[A-Za-z0-9-_]+){2}$", encoded)

def test_task_decode():
    test_task = Task(
        title="Test Task Title",
        description="Test Description",

        creator="John Doe",
        performers=["Test Performer One", "Test Performer Two"],
        tags=["Test Tag One", "Test Tag Two"],
    )

    jwt_hasher = JWTHasher(key='super_key', alg='HS256')
    jwt_hasher_interface = HasherInterface(jwt_hasher)

    encoded = jwt_hasher_interface.encode(test_task)
    decoded = Task(**jwt_hasher_interface.decode(encoded))

    assert decoded == test_task