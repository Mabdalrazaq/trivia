import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy.sql.expression import func
import random
import sys
from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate(selection,page):
  start=QUESTIONS_PER_PAGE*(page-1)
  end=start+QUESTIONS_PER_PAGE
  return selection[start:end]

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  cors=CORS(app)
  # '''
  # @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  # '''

  # '''
  # @TODO: Use the after_request decorator to set Access-Control-Allow
  # '''
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
    response.headers.add('Access-Control-Allow-Credentials','true')
    return response  


  # '''
  # @TODO: 
  # Create an endpoint to handle GET requests 
  # for all available categories.
  # '''

  @app.route('/categories')
  def retrieve_categories():
    categories=Category.query.all()
    return jsonify({
      'success':True,
      'categories':[category.format() for category in categories]
    })

  @app.route('/questions')
  def retrieve_questions():
    page=request.args.get('page',1,type=int)
    current_category=request.args.get('current_category')
    searchTerm=request.args.get('search_term')
    selection=[]
    if(current_category !='null' and current_category is not None):
      selection=Question.query.filter(Question.category==current_category).order_by(Question.id).all()
    elif(searchTerm is not None):
      selection=Question.query.filter(Question.question.ilike(f'%{searchTerm}%')).order_by(Question.id).all()
    else:
      selection=Question.query.order_by(Question.id).all()
    questions=paginate(selection,page)
    if(not len(questions)):
      abort(404)
    return jsonify({
      'success': True,
      'questions': [question.format() for question in questions],
      'total_questions': len(selection),
      'current_category': current_category,
      'categories': [category.format() for category in Category.query.all()]
    })

  # '''
  # @TODO: 
  # Create an endpoint to handle GET requests for questions, 
  # including pagination (every 10 questions). 
  # This endpoint should return a list of questions, 
  # number of total questions, current category, categories. 

  # TEST: At this point, when you start the application
  # you should see questions and categories generated,
  # ten questions per page and pagination at the bottom of the screen for three pages.
  # Clicking on the page numbers should update the questions. 
  # '''

  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
    question=Question.query.filter(Question.id==question_id).one_or_none()
    if question is None:
      abort(404)
    question.delete()
    return(jsonify({
      'success':True,
      'id':question_id
    }))

  # '''
  # @TODO: 
  # Create an endpoint to DELETE question using a question ID. 

  # TEST: When you click the trash icon next to a question, the question will be removed.
  # This removal will persist in the database and when you refresh the page. 
  # '''

  def search(searchTerm):
    selection=Question.query.filter(Question.question.ilike(f'%{searchTerm}%')).order_by(Question.id).all()
    questions=paginate(selection,1)
    return jsonify({
      'success':True,
      'questions':[question.format() for question in questions],
      'total_questions':len(selection),
      'current_category':None
    })

  @app.route('/questions',methods=['POST'])
  def create_or_search():
    data=request.get_json()
    question_text=data.get('question','')
    answer=data.get('answer','')
    difficulty=data.get('difficulty',1)
    category=data.get('category',5)
    searchTerm=data.get('searchTerm')
    if(searchTerm is not None):
      return search(searchTerm)
    try:
      question=Question(
        answer=answer,
        difficulty=difficulty,
        question=question_text,
        category=category
      )
      question.insert()
      return jsonify({
        'success':True,
        'created':question.id
      })
    except:
      print(sys.exc_info())
      abort(422)

  # '''
  # @TODO: 
  # Create an endpoint to POST a new question, 
  # which will require the question and answer text, 
  # category, and difficulty score.

  # TEST: When you submit a question on the "Add" tab, 
  # the form will clear and the question will appear at the end of the last page
  # of the questions list in the "List" tab.  
  # '''

  # '''
  # @TODO: 
  # Create a POST endpoint to get questions based on a search term. 
  # It should return any questions for whom the search term 
  # is a substring of the question. 

  # TEST: Search by any phrase. The questions list will update to include 
  # only question that include that string within their question. 
  # Try using the word "title" to start. 
  # '''

  @app.route('/categories/<int:category_id>/questions')
  def retrieve_questions_from_category(category_id):
    category=Category.query.filter_by(id=category_id).one_or_none()
    if category is None:
      abort(404)
    selection=Question.query.filter(Question.category==category_id).order_by(Question.id).all()
    questions=paginate(selection,1)
    return jsonify({
      'success':True,
      'questions':[question.format() for question in questions],
      'total_questions':len(selection),
      'current_category':category_id
    })


  # '''
  # @TODO: 
  # Create a GET endpoint to get questions based on category. 

  # TEST: In the "List" tab / main screen, clicking on one of the 
  # categories in the left column will cause only questions of that 
  # category to be shown. 
  # '''


  @app.route('/quizzes',methods=['POST'])
  def give_questions():
    data=request.get_json()
    previous_questions=data.get('previous_questions',[])
    category=data.get('quiz_category',0)
    questionQuery=Question.query
    print(category)
    if(category!=0):
      questionQuery=questionQuery.filter(Question.category==category)
    question=questionQuery.filter(~Question.id.in_(previous_questions)).order_by(func.random()).first()
    return jsonify({
      'success':True,
      'question':question.format() if question is not None else None
    })

  # '''
  # @TODO: 
  # Create a POST endpoint to get questions to play the quiz. 
  # This endpoint should take category and previous question parameters 
  # and return a random questions within the given category, 
  # if provided, and that is not one of the previous questions. 

  # TEST: In the "Play" tab, after a user selects "All" or a category,
  # one question at a time is displayed, the user is allowed to answer
  # and shown whether they were correct or not. 
  # '''

  # '''
  # @TODO: 
  # Create error handlers for all expected errors 
  # including 404 and 422. 
  # '''

  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      'success':False,
      'message':'not found',
      'error':404
    }),404
  
  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
      'success':False,
      'message':'bad request',
      'error':400
    }),400

  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      'success':False,
      'message':'unprocessable',
      'error':422
    }),422

  @app.errorhandler(405)
  def method_not_allowed(error):
    return jsonify({
      'success':False,
      'message':'method not allowed',
      'error':405
    }),405

  @app.errorhandler(500)
  def internal_error(error):
    return jsonify({
      'success':False,
      'message':'internal server error',
      'error':500
    }),500

  
  return app

    