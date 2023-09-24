import unittest

from app.app import app
from app.database.db import db, initialize_db


class BaseCase(unittest.TestCase):

    def setUp(self):

        self.app = app.test_client()

        app.config['TESTING'] = True  # Set TESTING to True before creating the app instance
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        db.init_app(app)
        db.create_all()

    def tearDown(self):

        db.session.remove()
        db.drop_all()