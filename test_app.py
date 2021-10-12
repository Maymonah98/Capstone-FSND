import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Movies, Actors


class CapstoneTestCase(unittest.TestCase):
    """This class represents the Capstone test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.casting_assistant_token_header= {'Authorization': 'Bearer ' + os.environ['casting_assistant_token']}
        self.casting_director_token_header={'Authorization': 'Bearer ' + os.environ['casting_director_token']}
        self.executive_producer_token_header= {'Authorization': 'Bearer ' + os.environ['executive_producer_token']}
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "casting_agency_test"
        self.database_path = "postgresql://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.new_movie={
            'title':'new title',
            'release_date':' 05, 01, 2021 ',
        }
        self.new_actor={
            'name':'new name',
            'age': 20,
            'gender':'female',
            'movie_id':1
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

#  GET /movies success
    def test_get_movies(self):
        res = self.client().get('/movies')
        data= json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(len(data['movies']))

#  GET /movies fail
    def test_404_movie_does_not_exist(self):
        res=self.client().get('/movies/None')
        data=json.loads(res.data)

        self.assertEqual(res.status_code,404)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'],'Not found')

# GET /actors success
    def test_get_actors(self):
        res = self.client().get('/actors')
        data= json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(len(data['actors']))

# GET /actors fail 
    def test_404_actor_does_not_exist(self):
        res=self.client().get('/actors/80')
        data=json.loads(res.data)

        self.assertEqual(res.status_code,404)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'],'Not found')

# POST /movies success
    def test_create_movie(self):
        res=self.client().post('/movies',json=self.new_movie,headers=self.casting_director_token_header)
        data=json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(len(data['movies']))

# POST /movies fail
    def test_404_if_movie_creation_not_found(self):
        res = self.client().post('/movies/',json={},headers=self.executive_producer_token_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code,404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not found')

# PATCH /movies/3 success
    def test_update_movie(self):
        res=self.client().patch('/movies/3',json=self.new_movie,headers=self.casting_director_token_header)
        data=json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['movie'])
# PATCH /movies/800 fail
    def test_404_if_updated_movie_not_found(self):
        res = self.client().patch('/movies/800',json=self.new_movie,headers= self.executive_producer_token_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code,404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not found')
    
# DELETE /movies/6 success
    # def test_delete_movie_success(self):
    #     res=self.client().delete('/movies/6', headers={
    #         "Authorization": 'bearer ' + self.executive_producer_token})
    #     data=json.loads(res.data)

    #     movie= Movies.query.filter(Movies.id==6).one_or_none()
        
    #     self.assertEqual(res.status_code,200)
    #     self.assertEqual(data['success'],True)
    #     self.assertEqual(data['delete'],6)
    #     self.assertEqual(movie,None)
    
# DELETE /movies/1000 fail
    def test_400_if_movie_does_not_exist(self):
        res = self.client().delete('/movies/1000',headers=self.executive_producer_token_header)
        data=json.loads(res.data)

        self.assertEqual(res.status_code,400)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'],'Bad request')
       
    
# RBAC tests
    
    def test_403_create_movie(self):
        res=self.client().post('/movies',json=self.new_movie,headers=self.casting_assistant_token_header)
        data=json.loads(res.data)

        self.assertEqual(res.status_code,403)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'],{'code': 'unauthorized', 'description': 'Permission not found.'})
    
    def test_401_create_movie(self):
        res=self.client().post('/movies',json=self.new_movie)
        data=json.loads(res.data)

        self.assertEqual(res.status_code,401)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'],{
            'code': 'authorization_header_missing',
            'description': 'Authorization header is expected.'
        })

      

    def test_401_delete_movie(self):
        res=self.client().delete('/movies/2')
        data=json.loads(res.data)
        
        self.assertEqual(res.status_code,401)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'],{
            'code': 'authorization_header_missing',
            'description': 'Authorization header is expected.'
        })

    

    


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
