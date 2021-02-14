import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Actor, Movie


class AgencyTestCase(unittest.TestCase):
    """This class represents the agency test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "agency_test"
        self.database_path = "postgres://{}/{}".format(
            'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.new_actor = {
            'name': 'Tom Cruise',
            'age': 58,
            'gender': 'Male'
        }

        self.new_actor_wrong_type = {
            'name': 'Tom Cruise',
            'age': '58',
            'gender': 'Male'
        }

        self.new_movie = {
            'title': 'Little Women',
            'release_date': '2019-03-04'
        }

        self.new_movie_wrong_type = {
            'title': 'Little Women',
            'release_date': 20190309
        }


        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    GET endpoint test cases for each test for successful operation and for expected errors.
    """
    def test_get_actors(self):
        res = self.client().get('/actors')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_422_if_fetching_actors_fails(self):
        res = self.client().get('/actors/100')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_get_movies(self):
        res = self.client().get('/movies')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_422_if_fetching_movies_fails(self):
        res = self.client().get('/movies/100')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    """
    POST endpoint test cases for each test for successful operation and for expected errors.
    """
    def test_create_new_actor(self):
        res = self.client().post('/actors', json=self.new_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_422_if_actor_creation_fails(self):
        res = self.client().post('/actors', json=self.new_actor_wrong_type)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)

    def test_create_new_movie(self):
        res = self.client().post('/movies', json=self.new_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_422_if_movie_creation_fails(self):
        res = self.client().post('/movies', json=self.new_movie_wrong_type)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)

    """
    PATCH endpoint test cases for each test for successful operation and for expected errors.
    """
    def test_patch_actor(self):
        res = self.client().patch('/actors/1', json=self.target_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_422_if_updating_actor_fails(self):
        res = self.client().patch('/actors/1', json=self.target_actor_wrong_type)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)

    def test_patch_movie(self):
        res = self.client().patch('/movie/1', json=self.target_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_422_if_updating_movie_fails(self):
        res = self.client().patch('/movie/1', json=self.target_movie_wrong_type)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)

    """
    DELETE endpoint test cases for each test for successful operation and for expected errors.
    """
    def test_delete_actor(self):
        res = self.client().delete('/actors/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_422_if_non_existing_actor_deletion_fails(self):
        res = self.client().delete('/actors/100')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)

    def test_delete_movie(self):
        res = self.client().delete('/movies/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_422_if_non_existing_movie_deletion_fails(self):
        res = self.client().delete('/movies/100')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
   

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
