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
        self.database_path = "postgresql://postgres:postgres@{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)
        self.new_question={
            'question':'How?',
            'answer':'Good',
            'category':5,
            'difficulty':100
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

    def test_retrieve_questions(self):
        res=self.client().get('/questions')
        data=json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))
        self.assertTrue(len(data['categories']))

    def test_error_retrieve_non_existent_page(self):
        res=self.client().get('/questions?page=10000')
        data=json.loads(res.data)

        self.assertEqual(res.status_code,404)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'],'not found')

    def test_delete_question(self):
        res=self.client().delete('/questions/9')
        data=json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertEqual(data['id'],9)

    def test_error_delete_non_existent_question(self):
        res=self.client().delete('questions/1000')
        data=json.loads(res.data)

        self.assertEqual(res.status_code,404)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'],'not found')

    def test_create_question(self):
        res=self.client().post('/questions',json=self.new_question)
        data=json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['created'])

    def test_error_create_question_bad_path(self):
        res=self.client().post('/questions/4',json=self.new_question)
        data=json.loads(res.data)

        self.assertEqual(res.status_code,405)
        self.assertEqual(data['success'],False)
        self.assertTrue(data['message'],'method not allowed')

    def test_search_questions(self):
        res=self.client().post('/questions',json={'searchTerm':'title'})
        data=json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'])

    def test_search_questions_none(self):
        res=self.client().post('/questions',json={'searchTerm':'hellllllllllp'})
        data=json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertFalse(len(data['questions']))
        self.assertEqual(data['total_questions'],0)
    
    def test_retrieve_questions_from_category(self):
        res=self.client().get('/categories/1/questions')
        data=json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'],0)
        self.assertEqual(data['current_category'],1)
    def test_retrieve_questions_from_non_existent_category(self):
        res=self.client().get('/categories/100/questions')
        data=json.loads(res.data)

        self.assertEqual(res.status_code,404)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'],'not found')

    def test_quizzes_get_question(self):
        res=self.client().post('/quizzes',json={'previous_questions':[],'quiz_category':0})
        data=json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertTrue(len(data['question']))
        self.assertEqual(data['success'],True)

    def test_quizzes_get_question(self):
        res=self.client().post('/quizzes',json={'previous_questions':[11,10],'quiz_category':6})
        data=json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertEqual((data['question']),None)
        self.assertEqual(data['success'],True)

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()