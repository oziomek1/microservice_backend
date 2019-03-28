from project import db
from project.api.models.user import User


def add_user(username, email, password):
    user = User(
        username=username,
        email=email,
        password=password,
    )
    db.session.add(user)
    db.session.commit()
    return user


def initialize_user_for_test():
    username = 'test'
    email = 'test@test.com'
    password = 'example_password'
    add_user(username=username, email=email, password=password)
    return username, email, password
