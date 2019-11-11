from django.test import TestCase
import unittest
import json
import jwt
import bcrypt

from django.test        import Client
from users.models       import Users
from unittest.mock  import patch, MagicMock

class UserSignInTest(unittest.TestCase) :
    
    def setUp(self) :
        password        = 'hello123'
        byted_password  = bytes(password, 'utf-8')
        hashed_password = bcrypt.hashpw(byted_password, bcrypt.gensalt())

        Users(
            first_name  = 'sunghun',
            last_name   = 'choo',
            email       = 'ufc@gmail.com',
            password    = hashed_password.decode('utf-8'),
            birth_year  = 1811,
            birth_month = 4,
            birth_day   = 10
        ).save()

    def tearDown(self) :
        Users.objects.get(email='ufc@gmail.com').delete()

    def test_email_sign_in(self):
        c = Client()

        user_info       = {'email' : 'ufc@gmail.com', 'password' : 'hello123'}
        response        = c.post('/users/signin', json.dumps(user_info), content_type='applications/json')
        self.assertEqual(response.status_code, 200)

    @patch('users.views.requests')
    def test_kakao_sign_in(self, mocked_requests) :
        c = Client()

        class FakeResponse:
            def json(self):
                return {
                    "id" : "11",
                    "properties" : {"nickname" : "BAM"},
                    "kakao_account" : {"email" : "gogo@gmail.com"}
                }

        mocked_requests.get = MagicMock(return_value = FakeResponse())
        header = {'HTTP_Authorization' : '1234ABCD'}
        response = c.get('/users/kakao', content_type='applications/json', **header)
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()   
