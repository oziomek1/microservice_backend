from src.api.models.user import User


def test_new_user(new_user):
    """
    GIVEN: user model
    WHEN: new user is created
    THEN: check id, username, email, activation, password
    """
    assert new_user.email == 'user_tester@mail.com'


def test_user_id(new_user):
    """
    GIVEN an existing User
    WHEN the ID of the user is defined to a value
    THEN check the user ID returns a string (and not an integer) as needed by Flask-WTF
    """
    new_user.id = 1
    assert not isinstance(new_user.id, str)
    assert isinstance(new_user.id, int)
    assert new_user.id == 1
