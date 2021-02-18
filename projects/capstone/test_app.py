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
        self.test_database_name = "agency_test"
        self.test_database_path = "postgres://{}/{}".format(
            'localhost:5432', self.test_database_name)
        setup_db(self.app, self.test_database_path)

        self.token_casting_assistant = os.environ['TOKEN_CASTING_ASSISTANT']
        self.token_casting_director = os.environ['TOKEN_CASTING_DIRECTOR']
        self.token_executive_producer = os.environ['TOKEN_EXECUTIVE_PRODUCER']

        self.header_casting_assistant = {
            'Authorization': 'Bearer {}'.format(self.token_casting_assistant)
        }
        self.header_casting_director = {
            'Authorization': 'Bearer {}'.format(self.token_casting_director)
        }
        self.header_executive_producer = {
            'Authorization': 'Bearer {}'.format(self.token_executive_producer)
        }

        self.new_actor = {
            'name': 'Nicholas Hoult',
            'age': 31,
            'gender': 'Male'
        }

        self.new_actor_2 = {
            'name': 'Emma Watson',
            'age': 33,
            'gender': 'Female'
        }

        self.new_movie = {
            'title': 'The Banker',
            'release_date': '2019-05-16'
        }

        self.new_movie_2 = {
            'title': 'Little Women',
            'release_date': '2019-03-04'
        }

        self.patch_actor = {
            'age': 40,
            'gender': 'Male'
        }

        self.patch_movie = {
            'release_date': '2021-12-31'
        }

        # #binds the app to the current context
        # with self.app.app_context():
        #     self.app.config['SQLALCHEMY_DATABASE_URI'] = self.test_database_path
        #     self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        #     self.db = SQLAlchemy()
        #     self.db.init_app(self.app)
        #     self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    GET endpoint test cases for each test for successful operation and for expected errors.
    """

    def test_get_actors(self):
        res = self.client().get('/actors', headers=self.header_casting_assistant)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_401_if_fetching_actors_without_token(self):
        res = self.client().get('/actors')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_get_movies(self):
        res = self.client().get('/movies', headers=self.header_casting_director)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_401_if_fetching_movies_without_token(self):
        res = self.client().get('/movies')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    """
    POST endpoint test cases for each test for successful operation and for expected errors.
    """
    def test_create_new_actor(self):
        res = self.client().post(
            '/actors',
            headers=self.header_casting_director,
            json=self.new_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_401_if_creating_actor_without_token(self):
        res = self.client().post('/actors', json=self.new_actor_2)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_create_new_movie(self):
        res = self.client().post(
            '/movies',
            headers=self.header_executive_producer,
            json=self.new_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_401_if_creating_movie_invalid_token(self):
        res = self.client().post(
            '/movies',
            headers=self.header_casting_assistant,
            json=self.new_movie_2)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    """
    PATCH endpoint test cases for each test for successful operation and for expected errors.
    """

    def test_patch_actor(self):
        res = self.client().patch(
            '/actors/2',
            headers=self.header_casting_director,
            json=self.patch_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_401_if_updating_actor_without_token(self):
        res = self.client().patch('/actors/2', json=self.patch_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_patch_movie(self):
        res = self.client().patch(
            '/movies/2',
            headers=self.header_executive_producer,
            json=self.patch_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_401_if_updating_movie_invalid_token(self):
        res = self.client().patch(
            '/movies/2',
            headers=self.header_casting_assistant,
            json=self.patch_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    """
    DELETE endpoint test cases for each test for successful operation and for expected errors.
    """

    def test_delete_actor(self):
        res = self.client().delete('/actors/1', headers=self.header_casting_director)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_401_if_deleting_actor_without_token(self):
        res = self.client().delete('/actors/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_delete_movie(self):
        res = self.client().delete('/movies/1', headers=self.header_executive_producer)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_401_if_deleting_movie_invalid_token(self):
        res = self.client().delete('/movies/1', headers=self.header_casting_assistant)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)


# Make the tests conveniently executable
if __name__ == '__main__':
    unittest.main()
