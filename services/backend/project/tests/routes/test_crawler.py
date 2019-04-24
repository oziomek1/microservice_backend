import json

from project.tests.base import BaseTestCase


class TestCrawlerService(BaseTestCase):

    def test_crawler_is_accessible(self):
        with self.client:
            response = self.client.post('/crawler/test_phrase')
            data = json.loads(response.data.decode(encoding='utf-8'))
            self.assertEqual(response.status_code, 202)
            self.assertEqual(list(data.keys()), ['Location', 'task_id'])
