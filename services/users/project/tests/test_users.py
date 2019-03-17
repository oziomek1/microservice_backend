import json
import unittest

from project.tests.utils import add_user
from project.tests.base import BaseTestCase


class TestUserService(BaseTestCase):
    def test_ping(self):
        """Ensure route is working correctly"""
        response = self.client.get('/users/ping')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn('ping', data['message'])
        self.assertIn('success', data['status'])

    def test_add_user(self):
        """Ensure new user can be added to database"""
        with self.client:
            response = self.client.post(
                '/users',
                data=json.dumps({
                    'username': 'Tom',
                    'email': 'tom@email.com',
                    'password': 'example_password',
                }),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn('tom@email.com was added!', data['message'])
            self.assertIn('success', data['status'])

    def test_add_user_invalid_json(self):
        """Ensure error with invalid json"""
        with self.client:
            response = self.client.post(
                '/users',
                data=json.dumps({}),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_user_invalid_json_keys_no_username(self):
        """Ensure error with invalid json key no username"""
        with self.client:
            response = self.client.post(
                '/users',
                data=json.dumps({
                    'email': 'wrong@email.com',
                    'password': 'example_password',
                }),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_user_invalid_json_keys_no_password(self):
        """Ensure error with invalid json key no password"""
        with self.client:
            response = self.client.post(
                '/users',
                data=json.dumps({
                    'username': 'wrong',
                    'email': 'wrong@email.com',
                }),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_user_invalid_json_keys_no_email(self):
        with self.client:
            response = self.client.post(
                '/users',
                data=json.dumps({
                    'username': 'wrong',
                    'password': 'example_password',
                }),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_user_duplicate_email(self):
        """Ensure error with duplicated email"""
        with self.client:
            self.client.post(
                '/users',
                data=json.dumps({
                    'username': 'Tom',
                    'email': 'tom@email.com',
                    'password': 'example_password',
                }),
                content_type='application/json',
            )
            response = self.client.post(
                '/users',
                data=json.dumps({
                    'username': 'Tom',
                    'email': 'tom@email.com',
                    'password': 'example_password',
                }),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Email already exists', data['message'])
            self.assertIn('fail', data['status'])

    def test_single_user(self):
        """Ensure get single user correctly"""
        user = add_user(
            username='Tom',
            email='tom@email.com',
            password='example_password',
        )
        with self.client:
            response = self.client.get(f'/users/{user.id}')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn('Tom', data['data']['username'])
            self.assertIn('tom@email.com', data['data']['email'])
            self.assertIn('success', data['status'])

    def test_single_user_no_id(self):
        """Ensure error with no id provided"""
        with self.client:
            response = self.client.get('/users/not_existing_id')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('User does not exist', data['message'])
            self.assertIn('fail', data['status'])

    def test_single_user_incorrect_id(self):
        """Ensure error with incorrect id"""
        with self.client:
            response = self.client.get('/users/-1')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('User does not exist', data['message'])
            self.assertIn('fail', data['status'])

    def test_multiple_users(self):
        """Ensure get multiple users correctly"""
        add_user(
            username='Tom',
            email='tom@email.com',
            password='example_password',
        )
        add_user(
            username='Jerry',
            email='jerry@email.com',
            password='example_password',
        )
        with self.client:
            response = self.client.get('/users')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data['data']['users']), 2)
            self.assertIn('Tom', data['data']['users'][0]['username'])
            self.assertIn('tom@email.com', data['data']['users'][0]['email'])
            self.assertIn('Jerry', data['data']['users'][1]['username'])
            self.assertIn('jerry@email.com', data['data']['users'][1]['email'])
            self.assertIn('success', data['status'])

    def test_main_route_empty(self):
        """Ensure main is empty when no users"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'{}', response.data)

    def test_main_add_user(self):
        """Ensure new user can be added"""
        with self.client:
            response = self.client.post(
                '/',
                data=dict(
                    username='tom',
                    email='tom@email.com',
                    password='example_password',
                ),
                follow_redirects=True
            )
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'{}', response.data)


if __name__ == '__main__':
    unittest.main()
