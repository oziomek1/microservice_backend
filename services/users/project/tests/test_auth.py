import json

from flask import current_app

from project import db
from project.api.models import User
from project.tests.base import BaseTestCase
from project.tests.utils import add_user


class TestAuthBlueprint(BaseTestCase):
    def test_user_registration(self):
        with self.client:
            response = self.client.post(
                '/auth/register',
                data=json.dumps({
                    'username': 'Tom',
                    'email': 'tom@email.com',
                    'password': 'example_password',
                }),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertTrue(response.content_type, 'application/json')
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Successfully registered.')
            self.assertTrue(data['auth_token'])

    def test_user_registration_duplicate_email(self):
        add_user(
            username='test',
            email='test@test.com',
            password='example_password',
        )
        with self.client:
            response = self.client.post(
                '/auth/register',
                data=json.dumps({
                    'username': 'test2',
                    'email': 'test@test.com',
                    'password': 'example_password',
                }),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('User already exists.', data['message'])
            self.assertIn('fail', data['status'])

    def test_user_registration_duplicate_username(self):
        add_user(
            username='test',
            email='test@test.com',
            password='example_password',
        )
        with self.client:
            response = self.client.post(
                '/auth/register',
                data=json.dumps({
                    'username': 'test',
                    'email': 'test2@test.com',
                    'password': 'example_password',
                }),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('User already exists.', data['message'])
            self.assertIn('fail', data['status'])

    def test_user_registration_invalid_json(self):
        with self.client:
            response = self.client.post(
                '/auth/register',
                data=json.dumps({}),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload', data['message'])
            self.assertIn('fail', data['status'])

    def test_user_registration_invalid_json_keys_no_username(self):
        with self.client:
            response = self.client.post(
                '/auth/register',
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

    def test_user_registration_invalid_json_keys_no_password(self):
        with self.client:
            response = self.client.post(
                '/auth/register',
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

    def test_user_registration_invalid_json_keys_no_email(self):
        with self.client:
            response = self.client.post(
                '/auth/register',
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

    def test_registered_user_login(self):
        username = 'test'
        email = 'test@test.com'
        password = 'example_password'
        add_user(username=username, email=email, password=password)
        with self.client:
            response = self.client.post(
                '/auth/login',
                data=json.dumps({
                    'email': email,
                    'password': password,
                }),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertTrue(response.content_type, 'application/json')
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Successfully logged in.')
            self.assertTrue(data['auth_token'])

    def test_not_registered_user_login(self):
        with self.client:
            response = self.client.post(
                '/auth/login',
                data=json.dumps({
                    'email': 'test@test.com',
                    'password': 'example_password',
                }),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertTrue(response.content_type, 'application/json')
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == 'User does not exist.')

    def test_valid_user_logout(self):
        username = 'test'
        email = 'test@test.com'
        password = 'example_password'
        add_user(username=username, email=email, password=password)
        with self.client:
            response = self.client.post(
                '/auth/login',
                data=json.dumps({
                    'email': email,
                    'password': password,
                }),
                content_type='application/json',
            )
            token = json.loads(response.data.decode())['auth_token']
            response = self.client.get(
                '/auth/logout',
                headers={
                    'Authorization': f'Bearer {token}',
                }
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Successfully logged out.')

    def test_invalid_user_logout(self):
        with self.client:
            response = self.client.get(
                '/auth/logout',
                headers={
                    'Authorization': f'Bearer invalid',
                }
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 401)
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == 'Invalid token. Log in again.')

    def test_invalid_logout_expired(self):
        username = 'test'
        email = 'test@test.com'
        password = 'example_password'
        add_user(username=username, email=email, password=password)
        current_app.config['TOKEN_EXPIRATION_SECONDS'] = -1
        with self.client:
            response = self.client.post(
                '/auth/login',
                data=json.dumps({
                    'email': email,
                    'password': password,
                }),
                content_type='application/json',
            )
            token = json.loads(response.data.decode())['auth_token']
            response = self.client.get(
                '/auth/logout',
                headers={
                    'Authorization': f'Bearer {token}',
                }
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 401)
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == 'Token expired. Log in again.')

    def test_invalid_logout_no_token(self):
        with self.client:
            response = self.client.get(
                '/auth/logout',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 403)
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == 'Provide valid auth token.')

    def test_user_valid_status(self):
        username = 'test'
        email = 'test@test.com'
        password = 'example_password'
        add_user(username=username, email=email, password=password)
        with self.client:
            response = self.client.post(
                '/auth/login',
                data=json.dumps({
                    'email': email,
                    'password': password,
                }),
                content_type='application/json',
            )
            token = json.loads(response.data.decode())['auth_token']
            response = self.client.get(
                '/auth/status',
                headers={
                    'Authorization': f'Bearer {token}',
                }
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertTrue(response.content_type, 'application/json')
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['data'] is not None)
            self.assertTrue(data['data']['username'] == username)
            self.assertTrue(data['data']['email'] == email)
            self.assertTrue(data['data']['active'])

    def test_user_invalid_status(self):
        with self.client:
            response = self.client.get(
                '/auth/status',
                headers={
                    'Authorization': f'Bearer invalid',
                }
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 401)
            self.assertTrue(response.content_type, 'application/json')
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == 'Invalid token. Log in again.')

    def test_invalid_logout_inactive(self):
        username = 'test'
        email = 'test@test.com'
        password = 'example_password'
        add_user(username=username, email=email, password=password)
        user = User.query.filter_by(email=email).first()
        user.active = False
        db.session.commit()

        with self.client:
            response = self.client.post(
                '/auth/login',
                data=json.dumps({
                    'email': email,
                    'password': password,
                }),
                content_type='application/json',
            )
            token = json.loads(response.data.decode())['auth_token']
            response = self.client.get(
                '/auth/logout',
                headers={
                    'Authorization': f'Bearer {token}',
                }
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 401)
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == 'Provide valid auth token.')

    def test_invalid_status_inactive(self):
        username = 'test'
        email = 'test@test.com'
        password = 'example_password'
        add_user(username=username, email=email, password=password)

        user = User.query.filter_by(email=email).first()
        user.active = False
        db.session.commit()

        with self.client:
            response = self.client.post(
                '/auth/login',
                data=json.dumps({
                    'email': email,
                    'password': password,
                }),
                content_type='application/json',
            )
            token = json.loads(response.data.decode())['auth_token']
            response = self.client.get(
                '/auth/status',
                headers={
                    'Authorization': f'Bearer {token}',
                }
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 401)
            self.assertTrue(response.content_type, 'application/json')
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == 'Provide valid auth token.')
