import unittest
import json
from app import app


class TestAPI(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_cypher_request(self):
        url = \
            '/api/?url=https://en.wikipedia.org/' + \
            'wiki/ROT13&q=To%20get%20to%20the%20other%20side'
        expected_message = \
            "Warning: String 'To get to the other side' " + \
            "was found on website https://en.wikipedia.org/wiki/ROT13 " + \
            "within the body tag"
        response = self.app.get(url)
        rv = json.loads(response.data)
        self.assertTrue(response.status_code == 200)
        self.assertEqual(rv['message'], expected_message)


if __name__ == '__main__':
    unittest.main()
