"""Message model tests."""

# run these tests like:
#
#    python -m unittest test_message_model.py


import os
from unittest import TestCase

from models import db, User, Message, Follows

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"


# Now we can import app

from app import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()

class MessageModelTestCase(TestCase):
    """Test model for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()
        Follows.query.delete()

        self.client = app.test_client()


    def test_message_model(self):
        """Does basic model work?"""
        # Does Message.create successfully create a new message given valid credentials?

        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.commit()

        m = Message(
            text="testing",
            user_id=u.id
        )

        db.session.add(m)
        db.session.commit()

        # User should have one message 
        self.assertEqual(len(u.messages), 1)

    def test_message_model_fail(self):
        """does basic model fail if validations aren't present?"""
        # Does Message.create fail to create a new message if any of the validations (e.g. uniqueness, non-nullable fields) fail?

        u = User(
            email="test2@test.com",
            username="test2user",
            password="HASHED_PASSWORD2"
        )

        db.session.add(u)
        db.session.commit()

        m = Message(
            user_id=u.id
        )

        db.session.add(m)
        with self.assertRaises(Exception):
            db.session.commit()
        
        db.session.rollback()

        self.assertEqual(len(u.messages), 0)