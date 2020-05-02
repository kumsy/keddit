import unittest

from server import app
# from model import db, example_data, connect_to_db_test

class FlaskRoutes(unittest.TestCase):
    """ Tests for my keddit app. """

    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage(self):
        result = self.client.get("/")
        self.assertIn(b"Keddit", result.data)
        self.assertNotIn(b"Facebook", result.data)
        self.assertNotIn(b"Twitter", result.data)

    def test_registration(self):
        result = self.client.get("/registration")
        self.assertIn(b'Join Today', result.data)
        self.assertNotIn(b"Leave Today", result.data)





if __name__ == '__main__':
    unittest.main()