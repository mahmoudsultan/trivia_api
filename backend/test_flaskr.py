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
        self.database_path = "postgresql:///trivia"
        setup_db(self.app, self.database_path)

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

    """
    GET /categories
    """
    def test_get_categories(self):
        response = self.client().get('/categories')
        response_json = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response_json['success'])
        self.assertEqual(response_json['total_count'], Category.query.count())
        self.assertIsInstance(response_json['categories'], dict)

    """
    GET /questions
    """
    def test_paginated_questions(self):
        response = self.client().get('/questions')
        response_json = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response_json['success'])
        self.assertEqual(response_json['total_questions'], Question.query.count())
        self.assertTrue(response_json['questions'])
        self.assertEqual(len(response_json['questions']), 10)

        self.assertTrue(response_json['categories'])
        self.assertTrue(response_json['current_category'])

    def test_404_if_page_doesnot_exist(self):
        response = self.client().get('/questions?page=1000')
        response_json = json.loads(response.data)

        self.assertFalse(response_json['success'])

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response_json['message'], 'resource not found.')

    """
    POST /questions
    """
    def test_create_questions_with_valid_input(self):
        mock_question_body = {
            'question': 'Question Title',
            'answer': 'Question Answer',
            'category': Category.query.first().id,
            'difficulty': 1
        }

        response = self.client().post('/questions', json=mock_question_body)
        response_json = json.loads(response.data)

        self.assertEqual(response.status_code, 201)
        self.assertTrue(response_json['success'])
        self.assertTrue(response_json['question'])

        self.assertEqual(response_json['question']['question'], mock_question_body['question'])
        self.assertEqual(response_json['question']['answer'], mock_question_body['answer'])
        self.assertEqual(response_json['question']['category'], mock_question_body['category'])
        self.assertEqual(response_json['question']['difficulty'], mock_question_body['difficulty'])

    def test_create_questions_without_question(self):
        mock_question_body = {
            'answer': 'Question Answer',
            'category': Category.query.first().id,
            'difficulty': 1
        }

        response = self.client().post('/questions', json=mock_question_body)
        response_json = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertFalse(response_json['success'])
        self.assertEqual(response_json['message'], 'bad request')

    def test_create_questions_without_answer(self):
        mock_question_body = {
            'question': 'Question Title',
            'category': Category.query.first().id,
            'difficulty': 1
        }

        response = self.client().post('/questions', json=mock_question_body)
        response_json = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertFalse(response_json['success'])
        self.assertEqual(response_json['message'], 'bad request')
    
    def test_create_questions_without_category(self):
        mock_question_body = {
            'question': 'Question Title',
            'answer': 'Question Answer',
            'difficulty': 1
        }

        response = self.client().post('/questions', json=mock_question_body)
        response_json = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertFalse(response_json['success'])
        self.assertEqual(response_json['message'], 'bad request')

    def test_create_questions_without_difficulty(self):
        mock_question_body = {
            'question': 'Question Title',
            'answer': 'Question Answer',
            'category': Category.query.first().id,
        }

        response = self.client().post('/questions', json=mock_question_body)
        response_json = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertFalse(response_json['success'])
        self.assertEqual(response_json['message'], 'bad request')

    def test_create_questions_with_invalid_category_id(self):
        mock_question_body = {
            'question': 'Question Title',
            'answer': 'Question Answer',
            'category': 10000000000,
            'difficulty': 1
        }

        response = self.client().post('/questions', json=mock_question_body)
        response_json = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertFalse(response_json['success'])
        self.assertEqual(response_json['message'], 'unprocessible entity')

    """
    DELETE /questions
    """
    # TODO: Uncomment to run test
    # def test_delete_question_with_valid_id(self):
    #     question_to_be_deleted = Question.query.order_by(Question.id.desc()).first()
    #     response = self.client().delete(f'/questions/{question_to_be_deleted.id}')
    #     response_json = json.loads(response.data)

    #     self.assertEqual(response.status_code, 200)
    #     self.assertTrue(response_json['success'])
    #     self.assertTrue(response_json['question'], question_to_be_deleted.format())

    def test_delete_question_with_invalid_id(self):
        question_to_be_deleted = Question.query.order_by(Question.id.desc()).first()
        response = self.client().delete(f'/questions/{question_to_be_deleted.id + 1}')
        response_json = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertFalse(response_json['success'])
    
    """
    POST /questions/search
    """
    def test_search_questions_with_search_term(self):
        response = self.client().post('/questions/search', json={ 'searchTerm': 'search' })
        response_json = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response_json['success'])
        self.assertIsInstance(response_json['questions'], list)

    def test_search_questions_without_search_term(self):
        response = self.client().post('/questions/search', json={})
        response_json = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertFalse(response_json['success'])

    """
    GET /categories/:id/questions
    """
    def test_get_question_in_category(self):
        response = self.client().get(f'/categories/{Category.query.first().id}/questions')
        response_json = json.loads(response.data)

        self.assertEqual(response.status_code, 200)

        self.assertTrue(response_json['success'])
        self.assertTrue(response_json['questions'])
        self.assertTrue(response_json['total_questions'])
        self.assertTrue(response_json['current_category'])
    
    def test_get_question_in_category_with_invalid_id(self):
        response = self.client().get('/categories/10000000000000/questions')
        response_json = json.loads(response.data)

        self.assertEqual(response.status_code, 404)

        self.assertFalse(response_json['success'])
        self.assertEqual(response_json['message'], 'resource not found.')

    """
    POST /quizz
    """
    def test_post_quizz(self):
        mock_body_params = {
            'quiz_category': Category.query.first().format(),
            'previous_questions': [Question.query.first().id]
        }

        response = self.client().post('/quizzes', json=mock_body_params)
        response_json = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response_json['success'])
        self.assertIsInstance(response_json['question'], dict)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()