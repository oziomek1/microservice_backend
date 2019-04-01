import json

from project.tests.base import BaseTestCase


class TestAdminService(BaseTestCase):

    def test_admin_is_accessible(self):
        with self.client:
            response = self.client.get('/admin')
            data = json.loads(response.data.decode())
            self.assertEqual('success', data['status'])
            self.assertEqual(response.status_code, 200)
