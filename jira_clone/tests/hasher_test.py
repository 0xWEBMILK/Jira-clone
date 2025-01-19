import pytest
import re


from jira_clone.app.auth.hashing import HasherInterface, JWTHasher
from jira_clone.app.models.models import User


def test_hasher_encode():
    test_user = User(
        username="super_username",
        password="super_password",
        email="super_email@super_domain.zone",
    )

    jwt_hasher = JWTHasher(key='super_key', alg='HS256')
    jwt_hasher_interface = HasherInterface(jwt_hasher)

    encoded = jwt_hasher_interface.encode(test_user)

    assert re.fullmatch(r"^[A-Za-z0-9-_]+(.[A-Za-z0-9-_]+){2}$", encoded)

def test_hasher_decode():
    test_user = User(
        username="super_username",
        password="super_password",
        email="super_email@super_domain.zone",
    )

    jwt_hasher = JWTHasher(key='super_key', alg='HS256')
    jwt_hasher_interface = HasherInterface(jwt_hasher)

    encoded = jwt_hasher_interface.encode(test_user)
    decoded = jwt_hasher_interface.decode(encoded)

    assert isinstance(decoded, User)