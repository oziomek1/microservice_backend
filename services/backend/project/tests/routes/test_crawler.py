import json

from project.tests.base import BaseTestCase


class TestCrawlerService(BaseTestCase):

    def test_crawler_is_accessible(self):
        with self.client:
            response = self.client.get('/crawler')
            data = json.loads(response.data.decode())
            self.assertEqual('success', data['status'])
            self.assertEqual(response.status_code, 200)
