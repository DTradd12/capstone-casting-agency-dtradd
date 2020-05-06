import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db

assistant_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjY3bE5XenRSWEpIaF8xWkFXOGdLcyJ9.eyJpc3MiOiJodHRwczovL2R0cmFkZC5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWU5Y2ZjNzNkZTQzMWEwYzhkNjdiYjNkIiwiYXVkIjoiQ2FzdGluZ0FnZW5jeSIsImlhdCI6MTU4ODcwMjI4MywiZXhwIjoxNTg4Nzg4NjgzLCJhenAiOiJwd2RnZGFxcDg5SXdkbnZnM2N3alpvbE14M0VIM3NhOSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiXX0.awYpPoYOxk-ZDlnmeDYNCLXkthlC9pKI2s7GFhNJBTaV4ETdgx7_6NGEfjLH5DMDWX0rUdkppxmraS0AjL58yJdjUP2HEwtkiFpe9qvggsQXRLlHis1bWyYFI3irg45Ctmlnm6BuBPLM-0rFQRP_t2BU_YxnmTTjy-NkohFBZKfxaM9T-VJPAfZBeLI0ilemtnYznUlfI7brEAKnGVAnc-mejH39eyAWyrkp5QeMdYMT8LGJrq0ybP38rCurEdx7-ZjAoqv22rN5tjHqKIcnp9a92nMzB64qy1ohB6yBGGQOMIij1qYZyr7aKJDOKKcyZjtz17lh_lvrtBb3onuz6A'
director_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjY3bE5XenRSWEpIaF8xWkFXOGdLcyJ9.eyJpc3MiOiJodHRwczovL2R0cmFkZC5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWViMTkwYTE1NGIxNGMwYzEyNzk3MDJiIiwiYXVkIjoiQ2FzdGluZ0FnZW5jeSIsImlhdCI6MTU4ODY5NjgxMiwiZXhwIjoxNTg4NzgzMjEyLCJhenAiOiJwd2RnZGFxcDg5SXdkbnZnM2N3alpvbE14M0VIM3NhOSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9yIiwiZWRpdDphY3RvciIsImVkaXQ6bW92aWUiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBvc3Q6YWN0b3IiXX0.bxRBQPrpSlPZojqeKSNdkvoVZOQ8IbnMCChx8agPQiAPYzXbGLHQfSK1LcBnnXCcRM_ozKsRGeUdpOllOt59h1aA6UquUScIru-ysx-5XJIeJywgbzK0n_jSormEGO8-vvjvIfdJYKKB0hGckMriEuI_bkdG2OsIfnD6mAlvt8zdiNuHH3PvhC_u2-ObbZqbB-caz8lVsgw2yg8a2Rb5yBeembuezSBPxlr6ArjF4DFLk6ufHp2RZn1Ll6Qg7PG72xosHqEMKjVB6Jet5CjbMV6a948geivm5jfML0NtoBxR7ZCkp9hUuitPp_KmTiIBN0-G1vwyWaC_ztGe2xMmQQ'
producer_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjY3bE5XenRSWEpIaF8xWkFXOGdLcyJ9.eyJpc3MiOiJodHRwczovL2R0cmFkZC5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWU5NDkyMTAyNGU0YmMwYmUzNzM1ZjI2IiwiYXVkIjoiQ2FzdGluZ0FnZW5jeSIsImlhdCI6MTU4ODY5NzQ2MiwiZXhwIjoxNTg4NzgzODYyLCJhenAiOiJwd2RnZGFxcDg5SXdkbnZnM2N3alpvbE14M0VIM3NhOSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9yIiwiZGVsZXRlOm1vdmllIiwiZWRpdDphY3RvciIsImVkaXQ6bW92aWUiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBvc3Q6YWN0b3IiLCJwb3N0Om1vdmllIl19.ZBUkhDbVByD6QxcW39vzz0L1jsdKaPqaAq_DqOuvEPZl2lQzifXx1pK8tHrAGbJOE-kdDhMLjjWONzTn-VFy870Gof1veLmzmO-BOAPX-UkpEsROtOodewubVYo20-vJtGv1XbMC83cBRBM_CEw9YAZ1yTXR0oU5nyBvr9wk4BeXBSKlOlTMjXRVlXOxRfxrU0pLU2-D5SWdpSExug1o0z1SqXp547hBkfnjvHDNMCf3WZw6vl2SJ6o5DtArkYlHN1UGNxbjZcFPv9Cu5PGyu7PCwJ6vNz3F6XCI0GsPcjLCV2vJPjr_4fU7V6g1E96tryXooqCXOgQl8aU5EUZ7Uw'


class CastingAgencyTestCase(unittest.TestCase):

    def setUp(self):
        self.APP = create_app()
        self.client = self.APP.test_client
        self.database_path = "postgresql://postgres:password@localhost:5432/castingagency_test"
        setup_db(self.APP, self.database_path)

        self.headers_casting_assistant = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {assistant_token}"
        }
        self.headers_casting_director = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {director_token}"
        }
        self.headers_executive_producer = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {producer_token}"
        }

        self.new_actor = {
            "name": "Actor TestActor",
            "age": 100,
            "gender": "Male/Female"
        }
        self.new_movie = {
            "title": "Movie TestMovie",
            "release_date": "5/18/1990"
        }

        with self.APP.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.APP)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        pass

####################################################################
    # PUBLIC/ NO PERMISSIONS
    def test_get_movies_and_actors_public(self):
        response = self.client().get('/')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])
        self.assertTrue(data['actors'])

    # CASTING ASSISTANT PERMISSIONS
    def test_get_movies_casting_assistant(self):
        response = self.client().get('/movies', headers=self.headers_casting_assistant)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])

    def test_get_actors_casting_assistant(self):
        response = self.client().get('/actors', headers=self.headers_casting_assistant)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])

    def test_create_new_actor_casting_assistant(self):
        res = self.client().post('/actors/create', headers=self.headers_casting_assistant,
                                 json=self.new_actor)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['message'], {'error': 'incorrect permissions', 'status code': 401})

#######################################################################################
    # CASTING DIRECTOR PERMISSIONS
    def test_create_new_actor_casting_director(self):
        res = self.client().post('/actors/create', headers=self.headers_casting_director,
                                 json=self.new_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_create_new_movie_casting_director(self):
        res = self.client().post('/movies/create', headers=self.headers_casting_director,
                                 json=self.new_movie)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['message'], {'error': 'incorrect permissions', 'status code': 401})

    def test_delete_actor_by_id_casting_director(self):
        response = self.client().delete('/actors/1', headers=self.headers_casting_director)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 1)

    def test_422_if_add_actor_fails_casting_director(self):
        response = self.client().post('/actors', headers=self.headers_casting_director, json=self.new_actor)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'method not allowed')

    def test_422_if_actor_does_not_exist_casting_director(self):
        res = self.client().delete('/actors/1000', headers=self.headers_casting_director)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

#################################################################################################################
    # EXECUTIVE PRODUCER PERMISSIONS
    def test_create_new_movies_executive_producer(self):
        res = self.client().post('/movies/create', headers=self.headers_executive_producer,
                                 json=self.new_movie)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_delete_movie_by_id_executive_producer(self):
        response = self.client().delete('/movies/1', headers=self.headers_executive_producer)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 1)

    def test_422_if_add_movie_fails_exec_producer(self):
        response = self.client().post('/movies', headers=self.headers_executive_producer, json=self.new_movie)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'method not allowed')

    def test_422_if_movie_does_not_exist_exec_producer(self):
        res = self.client().delete('/movies/1000', headers=self.headers_executive_producer)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')


if __name__ == "__main__":
    unittest.main()
