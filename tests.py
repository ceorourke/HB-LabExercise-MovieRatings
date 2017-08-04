import unittest
from server import app
from model import db, connect_to_db
from seed import load_users, load_movies, load_ratings


class RatingTests(unittest.TestCase):
    """Tests for ratings app"""

    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage(self):
        result = self.client.get("/")
        self.assertIn("Movies", result.data)
        self.assertIn("Users", result.data)


class RatingTestsDatabase(unittest.TestCase):
    """Flask tests that use the database."""

    def setUp(self):
        """Stuff to do before every test"""

        self.client = app.test_client()
        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'key'

        with self.client as c:
            with c.session_transaction() as session:
                session['user_id'] = 1

        connect_to_db(app, "postgresql:///ratingtestdb")

        db.create_all()
        load_users()
        load_movies()
        load_ratings

    def tearDown(self):
        """Stuff to do at the end of every test"""

        db.session.close()
        db.drop_all()

    def test_movie_page(self):
        result = self.client.get("/movies")
        self.assertIn("Movies", result.data)
        self.assertNotIn("Users", result.data)

    def test_user_page(self):
        result = self.client.get("/users")
        self.assertIn("Users", result.data)
        self.assertNotIn("Movies", result.data)

if __name__ == "__main__":
    unittest.main()
