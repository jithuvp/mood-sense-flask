import json

from app.tests.base_case import BaseCase

class TestUserLogin(BaseCase):

    def test_successful_login(self):
        # Given
        email = "Robjack@wxample.com"
        password = "mycoolpassword"
        payload = json.dumps({
            "email": email,
            "password": password
        })
        response = self.app.post(
            '/api/auth/signup', 
            headers={"Content-Type": "application/json"}, 
            data=payload)

        # When
        response = self.app.post(
            '/api/auth/login', 
            headers={"Content-Type": "application/json"}, 
            data=payload)

        # Then
        self.assertEqual(str, type(response.json['token']))
        self.assertEqual(200, response.status_code)

    def test_login_with_invalid_password(self):
        # Given
        email = "Robjack@wxample.com"
        password = "mycoolpassword"
        payload = {
            "email": email,
            "password": password
        }
        response = self.app.post('/api/auth/signup', headers={"Content-Type": "application/json"}, data=json.dumps(payload))

        # When
        payload['password'] = "myverycoolpassword"
        response = self.app.post('/api/auth/login', headers={"Content-Type": "application/json"}, data=json.dumps(payload))

        # Then
        self.assertEqual("Email or password invalid", response.json['message'])
        self.assertEqual(401, response.status_code)

