import json

from app.tests.base_case import BaseCase

class TestUserSignup(BaseCase):

    def test_successful_signup(self):
        # Given
        payload = json.dumps({
            "email": "Robjack@wxample.com",
            "password": "mycoolpassword"
        })

        # When
        response = self.app.post(
            '/api/auth/signup', 
            headers={"Content-Type": "application/json"}, 
            data=payload)

        # Then
        self.assertEqual(str, type(response.json['data']))
        self.assertEqual(200, response.status_code)

    def test_signup_with_non_existing_field(self):
        #Given
        payload = json.dumps({
            "username": "mycoolusername",
            "email": "Robjack@wxample.com",
            "password": "mycoolpassword"
        })

        #When
        with self.assertRaises(TypeError):
            response = self.app.post(
                '/api/auth/signup', 
                headers={"Content-Type": "application/json"}, 
                data=payload)
            self.assertEqual(500, response.status_code)

    def test_signup_without_email(self):
        #Given
        payload = json.dumps({
            "password": "mycoolpassword",
        })

        #When
        response = self.app.post(
            '/api/auth/signup', 
            headers={"Content-Type": "application/json"}, 
            data=payload)

        # Then
        self.assertEqual('Missing argument \'email\' in the body...', response.json['message'])
        self.assertEqual(400, response.status_code)

    def test_signup_without_password(self):
        #Given
        payload = json.dumps({
            "email": "Robjack@wxample.com",
        })

        #When
        response = self.app.post(
            '/api/auth/signup', 
            headers={"Content-Type": "application/json"}, 
            data=payload)
        
        # Then
        self.assertEqual('Missing argument \'password\' in the body...', response.json['message'])
        self.assertEqual(400, response.status_code)
        

    def test_creating_already_existing_user(self):
        #Given
        payload = json.dumps({
            "email": "Robjack@wxample.com",
            "password": "mycoolpassword"
        })
        response = self.app.post(
            '/api/auth/signup', 
            headers={"Content-Type": "application/json"}, 
            data=payload)

        # When
        response = self.app.post(
            '/api/auth/signup', 
            headers={"Content-Type": "application/json"}, 
            data=payload)

        # Then
        self.assertEqual('User already exists. Please Login...', response.json['message'])
        self.assertEqual(400, response.status_code)
