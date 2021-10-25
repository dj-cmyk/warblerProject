"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


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


class UserModelTestCase(TestCase):
    """Test model for users."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()
        Follows.query.delete()

        self.client = app.test_client()

        

    def test_user_model(self):
        """Does basic model work?"""

        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.commit()

        # User should have no messages & no followers
        self.assertEqual(len(u.messages), 0)
        self.assertEqual(len(u.followers), 0)



    def test_user_model_validations(self):
        """Does User.create fail to create a new user if any of the validations (e.g. uniqueness, non-nullable fields) fail?"""

        u = User(
            email="test@test.com",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
       
        with self.assertRaises(Exception):
            db.session.commit()
        
        db.session.rollback()
        

        u1 = User(
            email="test1@test.com",
            username="test1user",
            password="HASHED_PASSWORD1"
        )

        u2 = User(
            email="test2@test.com",
            username="test1user",
            password="HASHED_PASSWORD2"
        )

        db.session.add(u1)
        db.session.add(u2)
        with self.assertRaises(Exception):
            db.session.commit()
        
        db.session.rollback()



    def test_user_model_repr(self):
        """Does the repr method work as expected?"""

        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.commit()

        self.assertEqual(u.__repr__(), f"<User #{u.id}: testuser, test@test.com>")



    def test_user_model_not_following(self):
        """
        Does is_followed_by successfully detect when user1 is not followed by user2?
        Does is_following successfully detect when user1 is not following user2?
        """

        u1 = User(
            email="test1@test.com",
            username="test1user",
            password="HASHED_PASSWORD1"
        )

        u2 = User(
            email="test2@test.com",
            username="test2user",
            password="HASHED_PASSWORD2"
        )

        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()

        # User should have no messages & no followers
        self.assertFalse(u1.is_followed_by(u2))
        self.assertFalse(u2.is_followed_by(u1))
        self.assertFalse(u1.is_following(u2))
        self.assertFalse(u2.is_following(u1))


    def test_user_model_following(self):
        """
        Does is_followed_by successfully detect when user1 is followed by user2?
        Does is_following successfully detect when user1 is following user2?
        """

        u1 = User(
            email="test1@test.com",
            username="test1user",
            password="HASHED_PASSWORD1"
        )

        u2 = User(
            email="test2@test.com",
            username="test2user",
            password="HASHED_PASSWORD2"
        )

        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()

        u1.followers.append(u2)
        u2.followers.append(u1)
        db.session.commit()

        self.assertTrue(u1.is_followed_by(u2))
        self.assertTrue(u2.is_followed_by(u1))
        self.assertTrue(u1.is_following(u2))
        self.assertTrue(u2.is_following(u1))


    def test_user_model_authentication(self):
        """Does User.authenticate successfully return a user when given a valid username and password?"""

        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.commit()

        user = User.authenticate(u.username,u.password)
        self.assertTrue(user)
        

 
def test_user_model_authentication_invalid(self):
        """Does User.authenticate fail to return a user when the username is invalid?
        Does User.authenticate fail to return a user when the password is invalid? """

        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.commit()

        self.assertFalse(User.authenticate("wrongusername", u.password))
        self.assertFalse(User.authenticate(u.username, "wrongPassword"))
