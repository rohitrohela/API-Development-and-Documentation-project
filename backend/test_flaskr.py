import os
import unittest
import json

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        # self.app = Flask(__name__, instance_relative_config=True)
        self.database_name = "trivia_test"
        self.database_path = f'postgresql://{"postgres"}:{"postgres"}@{"localhost:5432"}/{self.database_name}'
        self.app = create_app(self.database_path)
        self.client = self.app.test_client

        # setup_db(self.app, self.database_path)

        # binds the app to the current context
        # with self.app.app_context():
        #     self.db = SQLAlchemy()
        #     self.db.init_app(self.app)
        #     # create all tables
        #     self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_get_category(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_get_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_get_questions_Fail(self):
        res = self.client().get('/questions?page=1254154875')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['message'], "Not found")

    def test_create_question(self):
        res = self.client().post('/questions', json={
            "question": "Here a new question string",
            "answer": "Here a new answer string",
            "difficulty": 1,
            "category": 3
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_create_question_Fail(self):
        res = self.client().post('/questions', json={
            "question": "Here a new question string",
            "answer": "Here a new answer string",
            "difficulty": 145824,
            "category": 3145214585
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], False)

    def test_search_question(self):
        res = self.client().post('/questions', json={
            "searchTerm": "new"
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_search_question_noResult(self):
        res = self.client().post('/questions', json={
            "searchTerm": "sfdsfsdfdsfsfdsfsdfdfdfdsfweghfhx!"
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['totalQuestions'], 0)

    def test_get_question_forCategories(self):
        res = self.client().get('categories/2/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['currentCategory'], "Art")

    def test_get_question_forCategories_Fail(self):
        res = self.client().get('categories/20sf/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Not found")

    def test_get_question_forCategories_NoResult(self):
        res = self.client().get('categories/201254/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Not found")

    def test_delete_question(self):
        # Get the id of created question by test
        res = self.client().post('/questions', json={
            "searchTerm": "Here a new question"
        })
        data = json.loads(res.data)

        if data['success']:  # If we have found the question, then delete it
            question_id = data['questions'][0]['id']
            deleteUrl = 'questions/' + str(question_id)
            res = self.client().delete(deleteUrl)
            data = json.loads(res.data)
            self.assertEqual(res.status_code, 200)
            self.assertEqual(data['success'], True)
            self.assertEqual(data['recordDeleted'], 1)

    def test_delete_question_Fail(self):
        res = self.client().delete('questions/12121212121221121212121212')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['recordDeleted'], 0)

    def test_Quiz_NextQuestion(self):
        res = self.client().post('/quizzes', json={
            "previous_questions": [20, 30, 21],
            "quiz_category": {
                "type": "Science",
                "id": "1"
            }
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_Quiz_NextQuestion_Fail(self):
        res = self.client().post('/quizzes', json={
            "previous_questions": ['a', 'b', 'c'],
            "quiz_category": {
                "type": "Science",
                "id": "4"
            }
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], False)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
