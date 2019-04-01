import json

from project.tests.base import BaseTestCase


class TestPingService(BaseTestCase):

    def test_index_empty(self):
        """Ensure main is empty"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'{}', response.data)

    def test_ping(self):
        """Ensure route is working correctly"""
        response = self.client.get('/ping')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn('ping', data['message'])
        self.assertIn('success', data['status'])
