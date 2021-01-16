import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}/{}".format(
            'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.new_question = {
            'question': 'What was the name of a fictional British boarding school of magic in Harry Potter',
            'answer': 'Hogwarts',
            'category': 5,
            'difficulty': 2}

        self.new_question_wrong_type = {
            'question': 'What was the name of a fictional British boarding school of magic in Harry Potter',
            'answer': 'Hogwarts',
            'category': 'Entertainment',
            'difficulty': 2}

        self.new_category = {
            'type': 'economy'
        }

        self.search_term = {
            'searchTerm': 'title'
        }

        self.non_existing_search_term = {
            'searchTerm': 'qwerty'
        }

        self.quiz_sample = {
            'previous_questions': [9, 12],
            'quiz_category': {
                'type': 'History',
                'id': '4'
            }

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
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_get_paginated_quetions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))

    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['categories']))

    def test_422_if_fetching_cateogory_fails(self):
        res = self.client().get('/categories/3')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_delete_question(self):
        res = self.client().delete('/questions/9')
        data = json.loads(res.data)

        question = Question.query.filter(Question.id == 9).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['categories']))
        self.assertTrue(data['current_category'])

    def test_422_if_non_existing_question_deletion_fails(self):
        res = self.client().delete('/questions/100')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)

    def test_create_new_question(self):
        res = self.client().post('/questions', json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_422_if_question_creation_fails(self):
        res = self.client().post('/questions', json=self.new_question_wrong_type)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)

    def test_search_question(self):
        res = self.client().post('/questions/search', json=self.search_term)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_404_if_search_fails(self):
        res = self.client().post('/questions/search', json=self.non_existing_search_term)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_get_categorized_questions(self):
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)
        picked_question = Question.query.filter(Question.category == 1).first()
        selection = Question.query.filter(Question.category == 1).all()
        questions = [question.format() for question in selection]

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['categories']))
        self.assertIn(picked_question.format(), data['questions'])
        self.assertListEqual(questions, data['questions'])

    def test_404_if_categorized_questions_fails(self):
        res = self.client().get('/categories/100/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_quizzes(self):
        res = self.client().post('/quizzes', json=self.quiz_sample)
        data = json.loads(res.data)
        selection = Question.query.filter(Question.category == 4).all()
        questions = [question.format() for question in selection]

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])
        self.assertIn(data['question'], questions)

    def test_404_if_quiz_creation_fails(self):
        res = self.client().post('/quizzes/1', json=self.quiz_sample)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
