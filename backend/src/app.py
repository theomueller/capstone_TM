import os
from flask import Flask, request, jsonify, abort
import json
from flask_cors import CORS

from models import  setup_db, Movie, Actor, Role
from auth import AuthError, requires_auth

def create_app(test_config=None):
    ''' To initiliase a env variable it should be EXPORT in the cmd line'''
    ''' Moreover don't forget to start the server'''
    
    database_path = os.environ['DATABASE_URL']
    if database_path.startswith("postgres://"):
        database_path = database_path.replace("postgres://", "postgresql://", 1)
    

    app = Flask(__name__)
    setup_db(app, database_path)
    CORS(app)

    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,POST,PUT,PATCH,DELETE,OPTIONS')
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        return response

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
    '''
    @app.route('/movies', methods=['GET'])
    @requires_auth('get:movies')
    def get_movies(_):
        movies_all = Movie.query.all()
        movies = [movie.short() for movie in movies_all]
        return jsonify({
            'success': True,
            'movies': movies
            }), 200

    '''
    GET /movies/id
    '''
    @app.route('/movies/<int:movie_id>', methods=['GET'])
    @requires_auth('get:movies')
    def role_movie(movie_id):
        movie = Movie.query.get(movie_id)
        roles_movie = Role.query.join(Actor).filter(Role.movie_id==movie_id).all()
        actors = [role.actor() for role in roles_movie]
        return jsonify({
            'success': True,
            'movies': movie.title,
            'actors': actors
            }), 200

    '''
    GET /actors
    '''
    @app.route('/actors', methods=['GET'])
    @requires_auth('get:actors')
    def get_actors(_):
        actors_all = Actor.query.all()
        actors = [actor.short() for actor in actors_all]
        return jsonify({
            'success': True,
            'actors': actors
            }), 200

    '''
    GET /actors/id
    '''
    @app.route('/actors/<int:actor_id>', methods=['GET'])
    @requires_auth('get:actors')
    def role_actor(actor_id):
        actor = Actor.query.get(actor_id)
        roles_actor = Role.query.join(Movie).filter(Role.actor_id==actor_id).all()
        movies = [role.movie() for role in roles_actor]
        return jsonify({
            'success': True,
            'actors': actor.name,
            'movies': movies
            }), 200
    '''
    DELETE /movies
    '''
    @app.route("/movies/<int:movie_id>", methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movie(_, movie_id):
        # check if the item is existing
        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
        try:
            if movie is None:
                abort(404)

            movie.delete()
            return jsonify({
                    'success': True,
                    'delete': movie.id
                }), 200
        except Exception:
            abort(422)

    '''
    DELETE /actors
    '''
    @app.route("/actors/<int:actor_id>", methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actor(_, actor_id):
        # check if the item is existing
        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
        #try:
        if actor is None:
            abort(404)

        actor.delete()
        return jsonify({
                'success': True,
                'delete': actor.id
            }), 200
        #except Exception:
        #    abort(422)

    '''
    POST /movies
    '''
    @app.route("/movies", methods=['POST'])
    @requires_auth('post:movies')
    def create_movie(payload):
        # get the body from the request
        body = request.get_json()
        try:
            # extract the title
            new_title = body.get('title')
            new_release =body.get('release')
            # add a test to avoid creating emppty drinks
            if (new_title is None or new_release is None):
                abort(400)

            movie = Movie(
                title=new_title,
                release=new_release)
            movie.insert()

            return jsonify({
                'success': True,
                'movies': [movie.short()],
            })
        except Exception:
            abort(422)

    '''
    POST /actors
    '''
    @app.route("/actors", methods=['POST'])
    @requires_auth('post:actors')
    def create_actor(payload):
        # get the body from the request
        body = request.get_json()
        try:
            # extract the title
            new_name = body.get('name')
            new_age =body.get('age')
            new_gender=body.get('gender')
            # add a test to avoid creating emppty drinks
            if (new_name is None 
            or new_age is None
            or new_gender is None):
                abort(400)

            actor = Actor(
                name=new_name,
                age=new_age,
                gender=new_gender)
            actor.insert()

            return jsonify({
                'success': True,
                'actors': [actor.short()],
            })
        except Exception:
            abort(422)

    '''
        PATCH /movies/<id>
    '''
    @app.route("/movies/<int:movie_id>", methods=['PATCH'])
    @requires_auth('patch:movies')
    def update_movie(_, movie_id):
        # check if the item is existing
        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
        # respond with 404 if movie is empty = <id> not founbd
        if movie is None:
            abort(404)
        # check the body
        try:
            body = request.get_json()
            movie.title = body.get('title', movie.title)
            if "release" in body:
                movie.release = body.get('release')
            movie.update()

            return jsonify({
                    'success': True,
                    'movies': [movie.short()],
                })
        except Exception:
            abort(422)

    '''
        PATCH /actors/<id>
    '''
    @app.route("/actors/<int:actor_id>", methods=['PATCH'])
    @requires_auth('patch:actors')
    def update_actors(_, actor_id):
        # check if the item is existing
        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
        # respond with 404 if actor is empty = <id> not founbd
        if actor is None:
            abort(404)
        # check the body
        try:
            body = request.get_json()
            if "name" in body:
                actor.name = body.get('name')
            if "gender" in body:
                actor.gender = body.get('gender')
            if "age" in body:
                actor.age = body.get('age')

            actor.update()

            return jsonify({
                    'success': True,
                    'actors': [actor.short()],
                })
        except Exception:
            abort(422)


    # Error Handling

    @app.errorhandler(405)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "method not allowed"
            }), 405

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
    implement error handler for AuthError
        error handler should conform to general task above
    '''

    @app.errorhandler(AuthError)
    def auth_error(message):
        return jsonify({
            'success': False,
            'error': message.status_code,
            'message': message.error['description']
        }), message.status_code

    return app


app = create_app()

if __name__ == "__main__":
    app.run()