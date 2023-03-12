import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db
from tokens import EXPIRED_TOKEN, CASTING_ASSISTANT_TOKEN, CASTING_DIRECTOR_TOKEN, EXECUTIVE_PRODUCER_TOKEN 

class CapstoneTestCase(unittest.TestCase):

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        DB_HOST = os.getenv('DB_HOST', '127.0.0.1:5432')
        DB_USER = os.getenv('DB_USER', 'postgres')
        DB_PASSWORD = os.getenv('DB_PASSWORD', 'postgres')
        DB_NAME = os.getenv('DB_NAME', 'capstone_test')
        # You can create a 'capstone_test' database or use another, just change the DB_NAME Environment variable
        self.database_path = 'postgresql+psycopg2://{}:{}@{}/{}'.format(DB_USER, DB_PASSWORD, DB_HOST, DB_NAME)
        setup_db(self.app, self.database_path)

        # Binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # Create all tables
            self.db.create_all()
            
    def tearDown(self):
        """Executed after reach test"""
        pass

    # ENDPOINT TESTING

    # Testing the root endpoint
    def test_root_endpoint(self):
        res = self.client().get('/')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['message'])

    # Test for root endpoint failure
    def test_root_endpoint_failure(self):
        res = self.client().post('/')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405) 
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])
        self.assertTrue(data['error'], 405)

    # The '/login' endpoint is just a redirect, 
    # so I will not be testing this endpoint

    # Test for Auth endpoint
    def test_auth_endpoint(self):
        res = self.client().get('/auth', headers={'Authorization':"Bearer {}".format(EXECUTIVE_PRODUCER_TOKEN)})
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['payload'])

    # Test for Auth endpoint failure
    def test_auth_endpoint_failure(self):
        res = self.client().get('/auth', headers={'Authorization':"Bearer {}".format(EXPIRED_TOKEN)})
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])
        self.assertTrue(data['error'])

    # Test for Actor creation endpoint
    def test_create_actor_endpoint(self):
        res = self.client().post('/actors', headers={'Authorization':"Bearer {}".format(EXECUTIVE_PRODUCER_TOKEN)},
            json={'name':'Dwayne "The Rock" Johnson', 'age':50, 'gender': 'Male'})
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actor'])
    
    # Test for Actor creation endpoint failure.
    # Failed because no authorization is given
    def test_create_actor_endpoint_failure(self):
        res = self.client().post('/actors',
            json={'name':'Dwayne "The Rock" Johnson'})
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])
        self.assertTrue(data['error'])

    # Test for Movie creation endpoint
    def test_create_movie_endpoint(self):
        res = self.client().post('/movies', headers={'Authorization':"Bearer {}".format(EXECUTIVE_PRODUCER_TOKEN)},
            json={'title':'San Andreas', 'release_date':'May 29th, 2015'})
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movie'])

    # Test for Movie creation endpoint failure, 
    # Failed because no authorization is given
    def test_create_movie_endpoint_failure(self):
        res = self.client().post('/movies',
            json={'title':'San Andreas'})
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])
        self.assertTrue(data['error'])

    # Test for Actor view endpoint
    def test_actor_view_endpoint(self):
        res = self.client().get('/actors', headers={'Authorization':"Bearer {}".format(EXECUTIVE_PRODUCER_TOKEN)})
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])

    # Test for Actor view endpoint failure,
    # Failed because no authorization is given
    def test_actor_view_endpoint_failure(self):
        res = self.client().get('/actors')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])
        self.assertTrue(data['error'])

    # Test for Movie view endpoint
    def test_movie_view_endpoint(self):
        res = self.client().get('/movies', headers={'Authorization':"Bearer {}".format(EXECUTIVE_PRODUCER_TOKEN)})
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])

    # Test for Movie view endpoint failure,
    # Failed because no authorization is given
    def test_movie_view_endpoint_failure(self):
        res = self.client().get('/movies')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])
        self.assertTrue(data['error'])

    # Test for editing Actor endpoint
    def test_a_edit_actor_endpoint(self):
        res = self.client().patch('/actors', headers={'Authorization':"Bearer {}".format(EXECUTIVE_PRODUCER_TOKEN)},
            json={'id':1, 'name':'Dwayne "The Rock" Johnson', 'age':50, 'gender': 'Male'})
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actor'])

    # Test for editing Actor endpoint failure,
    # Failed because no authorization is given
    def test_edit_actor_endpoint_failure(self):
        res = self.client().patch('/actors',
            json={'id':1,'name':'Dwayne "The Paper" Johnson', 'age':49, 'gender': 'Sigma Male'})
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])
        self.assertTrue(data['error'])

    # Test for editing Movie endpoint
    def test_a_edit_movie_endpoint(self):
        res = self.client().patch('/movies', headers={'Authorization':"Bearer {}".format(EXECUTIVE_PRODUCER_TOKEN)},
            json={'id':1,'title':'Pan Andreas', 'release_date':'May 28th, 2014'})
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movie'])

    # Test for editing Movie endpoint failure,
    # Failed because no authorization is given
    def test_edit_movie_endpoint_failure(self):
        res = self.client().patch('/movies',
            json={'id':1,'title':'Pan Andreas', 'release_date':'May 28th, 2014'})
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])
        self.assertTrue(data['error'])
    

    # RBAC TESTING

    # Casting Assistant Tests
    # Test for casting assistant role access
    def test_casting_assistant_role_access(self):
        res = self.client().get('/movies', headers={'Authorization':"Bearer {}".format(CASTING_ASSISTANT_TOKEN)})
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])

    # Test for casting assistant role access not allowed
    # Fails because casting assistang cannot add actors
    def test_casting_assistant_role_access_not_allowed(self):
        res = self.client().post('/actors', headers={'Authorization':"Bearer {}".format(CASTING_ASSISTANT_TOKEN)},
            json={'name':'Jack Black', 'age':50, 'gender': 'Male'})
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])
        self.assertTrue(data['error'])

    # Casting Director Tests
    # Test for casting director role access
    def test_casting_director_role_access(self):
        res = self.client().patch('/movies', headers={'Authorization':"Bearer {}".format(CASTING_DIRECTOR_TOKEN)},
            json={'id':1,'title':'The Great Big Shark', 'release_date':'April 20th, 2010'})
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movie'])

    # Test for casting director role access not allowed
    # Fails because casting director cannot add movies
    def test_casting_director_role_access_not_allowed(self):
        res = self.client().post('/movies', headers={'Authorization':"Bearer {}".format(CASTING_DIRECTOR_TOKEN)},
            json={'title':'San Andreas', 'release_date':'May 29th, 2015'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])
        self.assertTrue(data['error'])

    # Executive Producer Tests
    # Because the Executive Producer can do everything, 
    # There will be no failure tests, only the 2 endpoints 
    # that only the Executive Producer has access to are tested

    # Test for movie creation which only Executive Producers can do
    def test_executive_producer_role_access_create_movie(self):
        res = self.client().post('/movies', headers={'Authorization':"Bearer {}".format(EXECUTIVE_PRODUCER_TOKEN)},
            json={'title':'Scary Movie 5', 'release_date':'October 31st, 2022'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movie'])
    
    # Test for movie deletion which only Executive Producers can do
    # See DELETION ENDPOINT TESTING for why the _z_ is here
    def test_z_executive_producer_role_access_delete_movie(self):
        res = self.client().delete('/movies', headers={'Authorization':"Bearer {}".format(EXECUTIVE_PRODUCER_TOKEN)},
            json={'id':2})
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['deleted_movie_id'])

    

    # DELETION ENDPOINT TESTING
    # This goes last so that there is data for all of the other tests.
    # The _z_ is to make them test last, as they test in alphabetical order.
    # I could have used monolithic testing, but I am goofy, 
    # and I already wrote 300+ lines worth of tests.

    # Test for Actor delete endpoint
    def test_z_actor_delete_endpoint(self):
        res = self.client().delete('/actors', headers={'Authorization':"Bearer {}".format(EXECUTIVE_PRODUCER_TOKEN)},
            json={'id':1})
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['deleted_actor_id'])

    # Test for Actor delete endpoint failure
    # Failed because no authorization is given
    def test_z_actor_delete_endpoint_failure(self):
        res = self.client().delete('/actors', json={'id':1})
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])
        self.assertTrue(data['error'])

    # Test for Movie delete endpoint
    def test_z_movie_delete_endpoint(self):
        res = self.client().delete('/movies', headers={'Authorization':"Bearer {}".format(EXECUTIVE_PRODUCER_TOKEN)},
            json={'id':1})
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['deleted_movie_id'])

    # Test for Movie delete endpoint failure
    # Failed because no authorization is given
    def test_z_movie_delete_endpoint_failure(self):
        res = self.client().delete('/movies', json={'id':1})
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])
        self.assertTrue(data['error'])

    # ERROR TESTING

    # Error tests
    def test_400_bad_request(self):
        res = self.client().get('/400errortest')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])

    def test_404_not_found(self):
        res = self.client().get('/animalworldgorillatreelionlamppostelephantman')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])

    def test_422_unprocessable_entity(self):
        res = self.client().get('/422errortest')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])

    def test_500_internal_server_error(self):
        res = self.client().get('/500errortest')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 500)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])




# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()