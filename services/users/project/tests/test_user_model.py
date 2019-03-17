import unittest

from sqlalchemy.exc import IntegrityError

from project import db
from project.api.models import User
from project.tests.utils import add_user
from project.tests.base import BaseTestCase


class TestUserModel(BaseTestCase):
    def test_add_user(self):
        user = add_user(
            username='test',
            email='test@test.com',
            password='example_password',
        )
        self.assertTrue(user.id)
        self.assertEqual(user.username, 'test')
        self.assertEqual(user.email, 'test@test.com')
        self.assertTrue(user.active)
        self.assertTrue(user.password)

    def test_add_user_duplicate_username(self):
        add_user(
            username='test',
            email='test@test.com',
            password='example_password',
        )
        duplicate_user = User(
            username='test',
            email='test@test2.com',
            password='example_password',
        )
        db.session.add(duplicate_user)
        with self.assertRaises(IntegrityError):
            db.session.commit()

    def test_add_user_duplicate_email(self):
        add_user(
            username='test',
            email='test@test.com',
            password='example_password',
        )
        duplicate_user = User(
            username='testtest',
            email='test@test.com',
            password='example_password',
        )
        db.session.add(duplicate_user)
        with self.assertRaises(IntegrityError):
            db.session.commit()

    def test_to_json(self):
        user = add_user(
            username='test',
            email='test@test.com',
            password='example_password',
        )
        self.assertTrue(isinstance(user.to_json(), dict))

    def test_passwords_are_random(self):
        first_user = add_user('first', 'first@test.com', 'new_password')
        second_user = add_user('second', 'second@test.com', 'new_password')
        self.assertNotEqual(first_user.password, second_user.password)

    def test_encode_auth_token(self):
        user = add_user('test', 'test@test.com', 'test')
        auth_token = user.encode_auth_token(user.id)
        self.assertTrue(isinstance(auth_token, bytes))

    def test_decode_auth_token(self):
        user = add_user('test', 'test@test.com', 'test')
        auth_token = user.encode_auth_token(user.id)
        self.assertTrue(isinstance(auth_token, bytes))
        self.assertEqual(user.decode_auth_token(auth_token), user.id)


if __name__ == '__main__':
    unittest.main()
