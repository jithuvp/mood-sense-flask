import unittest

from app import app
from ..database.db import db, initialize_db


class BaseCase(unittest.TestCase):

    def setUp(self):
        self.app = app
        initialize_db(self.app)

    def tearDown(self):

        db.session.remove()
        db.drop_all()