"""User View tests."""

# run these tests like:
#
#    FLASK_ENV=production python -m unittest test_user_views.py


import os
from unittest import TestCase

from models import db, connect_db, Message, User

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"


# Now we can import app

from app import app, CURR_USER_KEY

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()

# Don't have WTForms use CSRF at all, since it's a pain to test

app.config['WTF_CSRF_ENABLED'] = False


class MessageViewTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()

        self.client = app.test_client()

        self.testuser = User.signup(username="testuser",
                                    email="test@test.com",
                                    password="testuser",
                                    image_url=None)

        db.session.commit()

    
    def test_list_users(self):
        """Page with listing of users.
        @app.route('/users')"""

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id

            
            resp = c.get("/users")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('testuser', html)

    
    def test_users_show(self):
        """Show user profile.
        @app.route('/users/<int:user_id>')"""
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id

            
            resp = c.get(f"/users/{self.testuser.id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('testuser', html)


    
    def test_show_following(self):
        """Show list of people this user is following.
        @app.route('/users/<int:user_id>/following')"""
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id

            
            resp = c.get(f"/users/{self.testuser.id}/following")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('following', html)


    
    def test_users_followers(self):
        """Show list of followers of this user.
        @app.route('/users/<int:user_id>/followers')"""
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id

            
            resp = c.get(f"/users/{self.testuser.id}/followers")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('followers', html)
    
    
    def test_profile(self):
        """Update profile for current user.
        @app.route('/users/profile', methods=["GET", "POST"])"""
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id

            
            resp = c.get("/users/profile")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('testuser', html)
    
    

    
    def test_add_follow(self):
        """Add a follow for the currently-logged-in user.
        @app.route('/users/follow/<int:follow_id>', methods=['POST'])"""
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id
            
            u1 = User(
            email="test1@test.com",
            username="test1user",
            password="HASHED_PASSWORD1"
            )
            db.session.add(u1)
            db.session.commit()

            resp = c.post(f"/users/follow/{u1.id}")

            self.assertEqual(resp.status_code, 302)

    
    def test_stop_following(self):
        """Have currently-logged-in-user stop following this user.
        @app.route('/users/stop-following/<int:follow_id>', methods=['POST'])"""
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id
            
            u1 = User(
            email="test1@test.com",
            username="test1user",
            password="HASHED_PASSWORD1"
            )
            db.session.add(u1)
            db.session.commit()

            add_follow = c.post(f"/users/follow/{u1.id}")

            resp = c.post(f"/users/stop-following/{u1.id}")

            self.assertEqual(resp.status_code, 302)


    def test_delete_user(self):
        """Delete user. @app.route('/users/delete', methods=["POST"])"""
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id

            resp = c.post("/users/delete")

            self.assertEqual(resp.status_code, 302)







# When you’re logged in, can you see the follower / following pages for any user?
# When you’re logged out, are you disallowed from visiting a user’s follower / following pages?
# When you’re logged in, can you add a message as yourself?
# When you’re logged in, can you delete a message as yourself?
# When you’re logged out, are you prohibited from adding messages?
# When you’re logged out, are you prohibited from deleting messages?
# When you’re logged in, are you prohibiting from adding a message as another user?
# When you’re logged in, are you prohibiting from deleting a message as another user?