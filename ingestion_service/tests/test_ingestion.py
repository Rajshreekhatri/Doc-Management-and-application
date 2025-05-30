import unittest
from app import create_app

class IngestionTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_ping(self):
        response = self.client.get('/ingestion/ping')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'is alive', response.data)

if __name__ == '__main__':
    unittest.main()
