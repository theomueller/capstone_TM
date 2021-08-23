import os
from flask import Flask, request, jsonify, abort
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Movie, Actor, Role
from .auth.auth import AuthError, requires_auth

def create_app(test_config=None):

    app = Flask(__name__)
    setup_db(app)
    CORS(app)


'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
!! Running this funciton will add one
'''


# ROUTES
#


# just to test if the app is running and if we have any
# error with dependencies
@app.route('/')
def hello_world():
    return jsonify({'message': 'Test server!'})
#


'''
GET /movies
        it should be a public endpoint
        it contains only the movies.short() data representation
    returns status code 200 and json {"success": True, "movies": movies}
    where movies is the list of movies
        or appropriate status code indicating reason for failure
'''


@app.route('/movies', methods=['GET'])
# @requires_auth('get:drinks') -> no need as it is publick
def get_moviess():
    movies_all = Movie.query.all()
    drinks = [drink.short() for drink in drinks_all]
    return jsonify({
        'success': True,
        'drinks': drinks
        }), 200


'''
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks}
    where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''


@app.route("/drinks-detail")
@requires_auth('get:drinks-detail')
def get_details_drinks(payload):
    drinks = [drink.long() for drink in Drink.query.all()]
    return jsonify({
        'success': True,
        'drinks': drinks
        }), 200


'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink}
    where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''


@app.route("/drinks", methods=['POST'])
@requires_auth('post:drinks')
def create_drink(payload):
    # get the body from the request
    body = request.get_json()
    try:
        # extract the title
        new_title = body.get('title')
        # extract the recipe and convert it in a array of strings
        # source: https://www.geeksforgeeks.org/
        #    python-convert-dictionary-object-into-string/
        new_recipe = json.dumps([body.get('recipe')])
        # add a test to avoid creating emppty drinks
        if (new_title is None or new_recipe is None):
            abort(400)

        drink = Drink(
            title=new_title,
            recipe=new_recipe)
        drink.insert()

        return jsonify({
            'success': True,
            'drinks': [drink.long()],
        })
    except Exception:
        abort(422)


'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink}
    where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''


@app.route("/drinks/<int:drink_id>", methods=['PATCH'])
@requires_auth('patch:drinks')
def update_drink(_, drink_id):
    # check if the item is existing
    drink = Drink.query.filter(Drink.id == drink_id).one_or_none()
    # respond with 404 if drink is empty = <id> not founbd
    if drink is None:
        abort(404)
    # check the body
    try:
        body = request.get_json()
        drink.title = body.get('title', drink.title)
        if "recipe" in body:
            drink.recipe = json.dumps([body.get('recipe')])
        drink.update()

        return jsonify({
                'success': True,
                'drinks': [drink.long()],
            })
    except Exception:
        abort(422)


'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id}
    where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''


@app.route("/drinks/<int:drink_id>", methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(_, drink_id):
    # check if the item is existing
    drink = Drink.query.filter(Drink.id == drink_id).one_or_none()
    try:
        if drink is None:
            abort(404)

        drink.delete()
        return jsonify({
                'success': True,
                'delete': drink.id
            }), 200
    except Exception:
        abort(422)


# Error Handling
'''
Example error handling for unprocessable entity
'''
'''
@TODO implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False,
                    "error": 404,
                    "message": "resource not found"
                    }), 404
@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422
'''


@app.errorhandler(405)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 405,
        "message": "method not allowed"
        }), 405


'''
@TODO implement error handler for 404
    error handler should conform to general task above
'''


@app.errorhandler(404)
def not_found(error):
    return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
    }), 404


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


@app.errorhandler(500)
def server_error(error):
    return jsonify({
        "success": False,
        "error": 500,
        "message": "INTERNAL SERVER ERROR"
        }), 500


'''
@TODO implement error handler for AuthError
    error handler should conform to general task above
'''


@app.errorhandler(AuthError)
def auth_error(message):
    return jsonify({
        'success': False,
        'error': message.status_code,
        'message': message.error['description']
    }), message.status_code


app = create_app()

if __name__ == "__main__":
    app.run()