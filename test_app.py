import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db

assistant_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjY3bE5XenRSWEpIaF8xWkFXOGdLcyJ9' \
                  '.eyJpc3MiOiJodHRwczovL2R0cmFkZC5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWU5Y2ZjNzNkZT' \
                  'QzMWEwYzhkNjdiYjNkIiwiYXVkIjoiQ2FzdGluZ0FnZW5jeSIsImlhdCI6MTU4ODgxMjA4MCwiZXhwIjo' \
                  'xNTg4ODk4NDgwLCJhenAiOiJwd2RnZGFxcDg5SXdkbnZnM2N3alpvbE14M0VIM3NhOSIsInNjb3BlIjoiIiw' \
                  'icGVybWlzc2lvbnMiOlsiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiXX0.AybsiBMMmIEg0_mUqL_Gn668-NA' \
                  'uojQCjvvdn41h31pM5JIiOUsuHd_pbibxcH9Pm0QXNHzYu7-ikD5DNDyJR1bhhBkZjYzOrdwuF50F7u7zl' \
                  'gSoHet41PgNld81BsSHs0c3-jNMZxOgXUivcwWp4I0nn2GNkBVmmg0lFKfSnbiOb2DXS-U3HTedJcbAVpA' \
                  'HqeiPBq7cZR9my5GznBjMtruLvCX4tD4ZN8knVEarTh6D1ddmzPyA9NNROgFpG1TrWbx1Q8t2GJGF8vfTm' \
                  '9DnKIOTXv8EUtipKJRK_4hjqc_yCesJhyrVtvQTgyionFtFiVRlc-QyXB9GYUFmllfSRw'
director_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjY3bE5XenRSWEpIaF8xWkFXOGdLcyJ9' \
                 '.eyJpc3MiOiJodHRwczovL2R0cmFkZC5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWViMTkwYTE1NGIxNGMw' \
                 'YzEyNzk3MDJiIiwiYXVkIjoiQ2FzdGluZ0FnZW5jeSIsImlhdCI6MTU4ODgxMjEyOCwiZXhwIjoxNTg4ODk4NT' \
                 'I4LCJhenAiOiJwd2RnZGFxcDg5SXdkbnZnM2N3alpvbE14M0VIM3NhOSIsInNjb3BlIjoiIiwicGVybWlzc2lv' \
                 'bnMiOlsiZGVsZXRlOmFjdG9yIiwiZWRpdDphY3RvciIsImVkaXQ6bW92aWUiLCJnZXQ6YWN0b3JzIiwiZ2V0Om' \
                 '1vdmllcyIsInBvc3Q6YWN0b3IiXX0.BXlM1_5rMraRZ5z1_OSnN4AdK3BknG8FdhPdYhUIl-1ZtzxCr_3cmfhx' \
                 'fMRCZ8hwh-I5uYhdx9XJujXv9lH4WSjQLwsK8cLQerup6PN9k-5LrrVNcToJhK99OHqtjVN0cWsA0VMMxfKPWG' \
                 '08Wt4s3oiCWnDPgW3gnvyRw2EM65h0EQMpAQfjT0Um78wf-tyhYwvNoCG1liADXHuxi4Xee9dcWQ6lPSIRJYQA' \
                 'WFopU5oxFJpwpze6xuX7czmMczLu-yToLtiCUw6hgTFwDjDq2SjD9zU8hfGYcZTnFGQry_l0-KcihTOdwnmM8q' \
                 'hLVtdu5WpSOWlFmOmWj43c4YS-bw'
producer_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjY3bE5XenRSWEpIaF8xWkFXOGdLcyJ9' \
                 '.eyJpc3MiOiJodHRwczovL2R0cmFkZC5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWU5NDkyMTAyNGU0YmMwY' \
                 'mUzNzM1ZjI2IiwiYXVkIjoiQ2FzdGluZ0FnZW5jeSIsImlhdCI6MTU4ODgxMjA0NiwiZXhwIjoxNTg4ODk4NDQ2L' \
                 'CJhenAiOiJwd2RnZGFxcDg5SXdkbnZnM2N3alpvbE14M0VIM3NhOSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOl' \
                 'siZGVsZXRlOmFjdG9yIiwiZGVsZXRlOm1vdmllIiwiZWRpdDphY3RvciIsImVkaXQ6bW92aWUiLCJnZXQ6YWN0b3' \
                 'JzIiwiZ2V0Om1vdmllcyIsInBvc3Q6YWN0b3IiLCJwb3N0Om1vdmllIl19.wXIyCQIOe78sH58KKeMrifVY5-6pO' \
                 'Wa5TxrX6c9BPNmkeBOjDq7L5dKEYk-OLDt8ZXXmW0JkIeMCtfQ5HCgmHR-e6qnezrclcki5WawhKBzpF-4zw3jdG' \
                 '9Z9uY7wLFqi6c41lD6I_YEmzI-psK5QeaH7s1uifEOFoyowO2ADbvyCyRRN9LxerAoJNU261VC4eq917CgujWOj' \
                 'LM2ETw0_DVlx17KjRq-UgqUUqFIIe8fB3k7_pYBLLDbudcDEhkA9Cl7OmC5LJNX6rHMQLCiwHzwWFdsuQkwmPBc' \
                 'u1xQkqK5qh0fcC6sqNxIIZZp2OYJRwj1daiA-9mtcGEBZ99m1kQ'


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

    # CASTING ASSISTANT PERMISSIONS
    def test_get_movies_casting_assistant(self):
        response = self.client().get('/movies', headers=self.headers_casting_assistant)

        self.assertEqual(response.status_code, 200)

    def test_get_actors_casting_assistant(self):
        response = self.client().get('/actors', headers=self.headers_casting_assistant)

        self.assertEqual(response.status_code, 200)

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
        res = self.client().post('/movies/create', headers=self.headers_casting_director, json=self.new_movie)
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
        res = self.client().post('/movies/create', headers=self.headers_executive_producer, json=self.new_movie)
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
