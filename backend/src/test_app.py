
import os
import unittest
import json
from sqlalchemy.sql.expression import true

from werkzeug.datastructures import Headers
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, db_drop_and_create_all


class CapstoneTestCase(unittest.TestCase):
    """This class represents the capstone test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.token_assistant = os.environ['token_assistant']
        self.token_director = os.environ['token_director']
        self.token_producer = os.environ['token_producer']

        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "testdb"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        """ Create instances to test post """
        self.new_movie = {"title":"movie unit", "release": "10/05/2002"}
        self.new_actor = {"name":"actor unit", "age":"10", "gender":"unit"}

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    

    def tearDown(self):
        db_drop_and_create_all()
        """Executed after reach test"""
        pass


    # ENDPOINTS GET /actors and /movies
    # Assistant Token
    def test_200_get_movies_with_token_assistant(self):
        res = self.client().get('/movies', headers={
            "Authorization": 'bearer ' + self.token_assistant})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['movies']))


    def test_200_get_actors_with_token_assistant(self):
        res = self.client().get('/actors', headers={
            "Authorization": 'bearer ' + self.token_assistant})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actors']))


    # Director Token
    def test_200_get_movies_with_token_director(self):
        res = self.client().get('/movies', headers={
            "Authorization": 'bearer ' + self.token_director})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['movies']))


    def test_200_get_actors_with_token_director(self):
        res = self.client().get('/actors', headers={
            "Authorization": 'bearer ' + self.token_director})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actors']))


    # Producer Token

    def test_200_get_movies_with_token_producer(self):
        res = self.client().get('/movies', headers={
            "Authorization": 'bearer ' + self.token_producer})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['movies']))

    
    def test_200_get_actors_with_token_producer(self):
        res = self.client().get('/actors', headers={
            "Authorization": 'bearer ' + self.token_producer})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actors']))


    # Error Behavior GET movies
    def test_404_get_movies_with_token_producer(self):
        res = self.client().get('/movies?1000', headers={
            "Authorization": 'bearer ' + self.token_producer})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    # Error Behavior GET actors
    def test_404_get_actors_with_token_producer(self):
        res = self.client().get('/actors?1000', headers={
            "Authorization": 'bearer ' + self.token_producer})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)   

    # ENDPOINTS Delete /actors/1 and /movies/1
    def test_200_delete_actors_with_token_producer(self):
        res = self.client().delete('/actors/1', headers={
            "Authorization": 'bearer ' + self.token_producer})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'],True)
        
    def test_200_delete_movies_with_token_producer(self):
        res = self.client().delete('/movies/1', headers={
            "Authorization": 'bearer ' + self.token_producer})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'],True)

    # Error behavior for delete actors
    def test_404_delete_actors_with_token_producer(self):
        res = self.client().delete('/actors/a', headers={
            "Authorization": 'bearer ' + self.token_producer})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'],'ressource not found')
        
    # Error behavior for delete movies
    def test_404_delete_movies_with_token_producer(self):
        res = self.client().delete('/movies/a', headers={
            "Authorization": 'bearer ' + self.token_producer})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'],'ressource not found')

    # ENDPOINTS POST /actors and /movies    
    def test_200_post_actors_with_token_producer(self):
        res = self.client().post('/actors',json=self.new_actor,headers={
            "Authorization": 'bearer ' + self.token_producer})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data['movies']))
        self.assertEqual(data['success'],True)
    
    def test_200_post_movies_with_token_producer(self):
        res = self.client().post(
            '/movies',
            json=self.new_movie,
            headers={
            "Authorization": 'bearer ' + self.token_producer})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(data['movies']))
        self.assertEqual(data['success'],True)

    # Error behavior Post /actors
    def test_422_post_actors_with_token_producer(self):
        res = self.client().post(
            '/actors',
            json={"name":"John Postmann", "age":"23", "gen": "male"},
            headers={
                "Authorization": 'bearer ' + self.token_producer})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'],'unprocessable')     

    # Error behavior Post /movies
    def test_422_post_actors_with_token_producer(self):
        res = self.client().post(
            '/movies',
            json={"release":"12/10/2020"},
            headers={
                "Authorization": 'bearer ' + self.token_producer})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'],'unprocessable') 

    # ENDPOINTS PATCH /actors and /movies 
    def test_200_patch_actors_with_token_producer(self):
        res = self.client().patch(
            '/actors/2',
            json={"name":"John Unit"},
            headers={
                "Authorization": 'bearer ' + self.token_producer})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'],True)
    
    def test_200_patch_movies_with_token_producer(self):
        res = self.client().patch(
            '/movies/2',
            json={"title":"Movie Unit"},
            headers={
                "Authorization": 'bearer ' + self.token_producer})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200, data)
        self.assertEqual(data['success'],True)

    # Error behavior Patch /actors
    def test_422_patch_actors_with_token_producer(self):
        res = self.client().patch(
            '/actors/2',
           # json={"name":"John Unit"},
            headers={
                "Authorization": 'bearer ' + self.token_producer})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'],'unprocessable') 

    # Error behavior Patch /movies
    def test_422_patch_movies_with_token_producer(self):
        res = self.client().patch(
            '/movies/2',
            #json={"title":"Movie Unit"},
            headers={
                "Authorization": 'bearer ' + self.token_producer})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'],'unprocessable') 

    # TEST Role Based Access Control for each role
    # Test Get without token !
    def test_get_movies_without_token(self):
        res = self.client().get('/movies', headers={
            "Authorization": 'bearer '})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)


    # Test Delete by Assistant
    def test_403_delete_movies_with_token_assistant(self):
        res = self.client().delete('/movies/2', headers={
            "Authorization": 'bearer ' + self.token_assistant})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'],False)

    # Test Post by Assistant
    def test_403_post_movies_with_token_assistant(self):
        res = self.client().post(
            '/movies',
            json=self.new_movie,
            headers={
            "Authorization": 'bearer ' + self.token_producer})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'],False)

    # Test Delete Movie by Director
    def test_403_delete_movies_with_token_director(self):
        res = self.client().delete('/movies/2', headers={
            "Authorization": 'bearer ' + self.token_director})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'],False)

if __name__ == "__main__":
    unittest.main()