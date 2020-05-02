import unittest, json, pprint

from server import app
from flask_bcrypt import Bcrypt
from model import db, example_data, connect_to_db

class FlaskRoutes(unittest.TestCase):
    """ Tests for my keddit app. """

    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True

        with open('config/config.json', 'r') as f:
            config = json.load(f)
        app.config['SECRET_KEY'] = config["secret_key"]["keddit"]

    def test_landingpage(self):
        result = self.client.get("/")
        self.assertEqual(result.status_code, 200)
        self.assertIn(b"Keddit", result.data)
        self.assertNotIn(b"Facebook", result.data)
        self.assertNotIn(b"Twitter", result.data)

    def test_registration(self):
        result = self.client.get("/registration")
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'Join Today', result.data)
        self.assertIn(b'Sign Up', result.data)
        self.assertIn(b'Confirm Password', result.data)
        self.assertNotIn(b"Leave Today", result.data)

    def test_login_route(self):
        result = self.client.get("/login")
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'Welcome home. We have snacks.', result.data)
        self.assertIn(b'Log In', result.data)
        self.assertNotIn(b"Log Out", result.data)



class UsersTestDatabase(unittest.TestCase):
    """ Flask tests that use my test database. """

    def setUp(self):
        """ Set up before each test. """

        # Set flask client
        self.client = app.test_client()

        # Show Flask errors that happen during tests
        app.config['TESTING'] = True

        # Connect to test database
        connect_to_db(app)
        # connect_to_db_test(app, "postgresql:///testdb")

        # Create tables and add sample data
        db.create_all()
        # example_data()

    def tearDown(self):
        """ Perform at the end of each test. """

        db.session.close()
        db.drop_all()


    def test_user_login(self):
        with self.client:
            response = self.client.post('/login', 
            data={'email': 'admin@kristen.com', 'password': 'admin'})
            self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()