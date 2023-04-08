import pytest
from datetime import datetime

from newapp import User

@pytest.fixture(scope="module")
def new_user():
    return User.create("testuser@example.com", "testpass", "testuser")

def test_create(new_user):
    assert new_user.email_id == "testuser@example.com"
    assert new_user.username == "testuser"
    assert new_user.get_id() is not None

def test_find_by_email_id(new_user):
    user = User.find_by_email_id("testuser@example.com")
    assert user is not None
    assert user.get_id() == new_user.get_id()


def test_find_by_username(new_user):
    user = User.find_by_username("testuser")
    assert user is not None
    assert user.get_id() == new_user.get_id()

def test_get(new_user):
    user = User.get(new_user.get_id())
    assert user is not None
    assert user.get_id() == new_user.get_id()

def test_update_profile(new_user):
    user = User.update_profile(new_user, "new about", "http://example.com/image.jpg", [])
    assert user is not None
    assert user.get_id() == new_user.get_id()
    assert user.about == "new about"
    assert user.profile_image_url == "http://example.com/image.jpg"
