import json
import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
import random
import path
import sys
from backend.models import setup_db, Question, Category, db

QUESTIONS_PER_PAGE = 2


def create_app(dbPath=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    setup_db(app, dbPath)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    CORS(app, resources={r"*": {"origins": '*'}})
    # CORS(app)
    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """

    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type, Authorization"
        )
        response.headers.add(
            "Access-Control-Allow-Headers", "GET, POST, DELETE"
        )
        return response

    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """

    def paginate_questions(req):
        request_page = req.args.get("page", 1, type=int)
        selection = Question.query.paginate(page=request_page, per_page=QUESTIONS_PER_PAGE, error_out=True, max_per_page=QUESTIONS_PER_PAGE).items
        current_page = [question.format() for question in selection]
        return current_page

    @app.route("/categories", methods=["GET"])
    # @cross_origin
    def get_categories():
        all_category = {}
        for category in Category.query.all():
            all_category[str(category.id)] = category.type

        return jsonify(
            {
                "success": True,
                "categories": all_category,
            }
        )

    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """

    def get_questions(request):
        current_questions = paginate_questions(request)
        if len(current_questions) == 0:
            abort(404)

        all_category = {}
        for category in Category.query.all():
            all_category[str(category.id)] = category.type

        return jsonify(
            {
                "success": True,
                "questions": current_questions,
                "totalQuestions": len(current_questions),
                "categories": all_category
            }
        )

    def save_question(req):
        success = True
        try:
            question = Question(
                question=req['question'],
                answer=req['answer'],
                difficulty=req['difficulty'],
                category=req['category']
            )
            db.session.add(question)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            success = False
        finally:
            db.session.close()
        return jsonify(
            {
                "success": success
            }
        )

    def search_question(searchTerm):
        searchResult = Question.query.filter(Question.question.ilike('%' + searchTerm + '%')).all()
        questions = [question.format() for question in searchResult]

        return jsonify(
            {
                "success": True,
                "questions": questions,
                "totalQuestions": len(questions)
            }
        )

    @app.route("/questions", methods=["GET", "POST"])
    # @cross_origin
    def process_questions():
        if request.method == "GET":
            return get_questions(request)
        elif request.method == "POST":
            req_json = request.get_json()

            if "searchTerm" in str(req_json):
                searchTerm = req_json['searchTerm']
                return search_question(searchTerm)
            else:
                return save_question(request.get_json())

    @app.route("/categories/<int:cat_id>/questions", methods=["GET"])
    # @cross_origin
    def get_questions_for_category(cat_id):
        current_questions = paginate_questions(request, Question.query.filter(Question.category == cat_id).all())

        categories = Category.query.filter(Category.id == cat_id).one_or_none()
        if categories is None:
            abort(404)

        return jsonify(
            {
                "success": True,
                "questions": current_questions,
                "totalQuestions": len(current_questions),
                "currentCategory": categories.type
            }
        )

    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """

    @app.route("/questions/<int:ques_id>", methods=["DELETE"])
    def delete_question(ques_id):
        success = True
        recordDeleted = 0
        try:
            question = Question.query.filter_by(id=ques_id).one_or_none()
            if question is not None:
                question.delete()
                db.session.commit()
                recordDeleted = 1
            else:
                success = False
        except Exception as e:
            db.session.rollback()
            success = False
        finally:
            db.session.close()
        return jsonify(
            {
                "success": success,
                "recordDeleted": recordDeleted
            }
        )

    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """

    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """

    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """

    @app.route("/quizzes", methods=["POST"])
    def get_next_question():
        success = True
        result = ""
        try:
            req_json = request.get_json()
            query = []

            if len(req_json['previous_questions']) != 0:
                query.append(Question.id.not_in(req_json['previous_questions']))

            quiz_cat = req_json['quiz_category']
            if quiz_cat['type'] != 'click':
                query.append(Question.category == int(quiz_cat['id']))

            # questions = Question.query.filter(Question.id.not_in(prev_ques), Question.category == quiz_cat).first()
            questions = Question.query.filter(*query).first()

            if questions is not None:
                result = questions.format()
        except Exception as e:
            success = False
        finally:
            return jsonify(
                {
                    "success": success,
                    "questions": result
                }
            )

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "message": "unprocessable",
            "error": 422,
        }), 422

    return app
