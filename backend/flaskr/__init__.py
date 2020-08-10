import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category, db

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  CORS(app)

  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST,PUT,DELETE,OPTION,HEAD')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')

    return response

  def format_categories(categories):
    return { category.id: category.type for category in categories }

  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/categories', methods=['GET'])
  def categories():
    categories = Category.query.all()

    return jsonify({
      'categories': format_categories(categories),
      'success': True,
      'total_count': len(categories)
    })

  '''
    @TODO: 
    Create an endpoint to handle GET requests for questions, 
    including pagination (every 10 questions). 
    This endpoint should return a list of questions, 
    number of total questions, current category, categories. 

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions. 
  '''
  @app.route('/questions', methods=['GET'])
  def questions():
    page = request.args.get('page', 1, type=int)
    start = QUESTIONS_PER_PAGE * (page - 1)

    questions_in_page = Question.query.limit(QUESTIONS_PER_PAGE).offset(start).all()
    total_questions = Question.query.count()

    if not len(questions_in_page):
      abort(404)

    categories = Category.query.all()

    return jsonify({
      'success': True,
      'questions': [question.format() for question in questions_in_page],
      'total_questions': total_questions,
      'categories': format_categories(categories),
      'current_category': categories[0].id
    })

  '''
    @TODO: 
    Create an endpoint to DELETE question using a question ID. 

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
    question = Question.query.get(question_id)

    if not question:
      abort(404)

    try:
      db.session.delete(question)
      db.session.commit()
    except:
      db.session.rollback()
      abort(500)
    finally:
      db.session.close()
    
    return jsonify({
      'success': True,
      'question': question.format()
    })

  '''
    @TODO: 
    Create an endpoint to POST a new question, 
    which will require the question and answer text, 
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab, 
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.  
  '''
  @app.route('/questions', methods=['POST'])
  def create_question():
    body_params = request.get_json()
    question = body_params.get('question', None)
    answer = body_params.get('answer', None)
    category = body_params.get('category', None)
    difficulty = body_params.get('difficulty', None)

    if not question or not answer or not category or not difficulty:
      abort(400)

    selected_category = Category.query.get(category)

    if not selected_category:
      abort(422)

    created_question = Question(question, answer, category, difficulty)
    formated_question = created_question.format()

    try:
      db.session.add(created_question)
      db.session.commit()
    except:
      db.session.rollback()
      abort(500)
    finally:
      db.session.close()

    return jsonify({
      'success': True,
      'question': formated_question
    }), 201


  '''
    @TODO: 
    Create a POST endpoint to get questions based on a search term. 
    It should return any questions for whom the search term 
    is a substring of the question. 

    TEST: Search by any phrase. The questions list will update to include 
    only question that include that string within their question. 
    Try using the word "title" to start. 
  '''
  @app.route('/questions/search', methods=['POST'])
  def search_questions():
    search_term = request.get_json().get('searchTerm', None)

    if not search_term:
      abort(400)

    matched_questions = Question.query.filter(Question.question.ilike(f'%{search_term}%')).all()
    
    return jsonify({
      'success': True,
      'total_questions': len(matched_questions),
      'questions': [question.format() for question in matched_questions]
    })

  '''
    @TODO: 
    Create a GET endpoint to get questions based on category. 

    TEST: In the "List" tab / main screen, clicking on one of the 
    categories in the left column will cause only questions of that 
    category to be shown. 
  '''
  @app.route('/categories/<int:category_id>/questions', methods=['GET'])
  def category_questions(category_id):
    category = Category.query.get(category_id)

    if not category:
      abort(404)

    category_questions = Question.query.filter_by(category=category_id).all()

    return jsonify({
      'success': True,
      'questions': [question.format() for question in category_questions],
      'total_questions': len(category_questions),
      'current_category': category.format()
    })


  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''
  @app.route('/quizzes', methods=['POST'])
  def quizz():
    body_params = request.get_json()
    category = body_params['quiz_category']['id']
    previous_questions = body_params['previous_questions']

    available_questions = Question.query.filter(Question.category==category).filter(~Question.id.in_(previous_questions)).all()
    
    if not len(available_questions):
      return jsonify({
        'success': True,
        'question': None
      })

    random_question = random.choice(available_questions)
    return jsonify({
      'success': True,
      'question': random_question.format()
    })

  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  @app.errorhandler(404)
  def not_found(_error):
    return jsonify({
      'success': False,
      'error': 404,
      'message': 'resource not found.'
    }), 404
  
  @app.errorhandler(400)
  def bad_request(_error):
    return jsonify({
      'success': False,
      'error': 400,
      'message': 'bad request'
    }), 400

  @app.errorhandler(422)
  def unprocessible_entity(_error):
    return jsonify({
      'success': False,
      'error': 422,
      'message': 'unprocessible entity'
    }), 422
  
  @app.errorhandler(500)
  def internal_server_error(_error):
    return jsonify({
      'success': False,
      'error': 500,
      'message': 'internal server error'
    }), 500

  return app

    