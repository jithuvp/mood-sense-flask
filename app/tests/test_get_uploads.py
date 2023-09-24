import json

from app.tests.base_case import BaseCase

class TestGetUpload(BaseCase):

    def test_get_uploads_response(self):
        # Given
        email = "Robjack@wxample.com"
        password = "mycoolpassword"
        user_payload = json.dumps({
            "email": email,
            "password": password
        })

        response = self.app.post(
            '/api/auth/signup', 
            headers={"Content-Type": "application/json"}, 
            data=user_payload)
        response = self.app.post(
            '/api/auth/login', 
            headers={"Content-Type": "application/json"}, 
            data=user_payload)
        login_token = response.json['token']


        upload_payload = {
            "state": "Happy",
            "lat": -55,
            "long": 76.5
        }

        response = self.app.post(
            '/api/users/1/uploads',
            headers={"Content-Type": "application/json", "Authorization": f"Bearer {login_token}"},
            data=json.dumps(upload_payload))

        # When
        response = self.app.get(
            '/api/users/1/uploads',
            headers={"Content-Type": "application/json", "Authorization": f"Bearer {login_token}"})

        self.assertEqual(200, response.status_code)
        
        added_upload = response.get_json()[0]

        # Then
        self.assertEqual(upload_payload['state'].lower(), added_upload['state'])
        self.assertEqual(dict, type(added_upload['location']))
        self.assertEqual(added_upload['user_id'], 1)
        self.assertEqual(200, response.status_code)


    def test_response_with_invalid_user_id(self):
        # Given
        email = "Robjack@wxample.com"
        password = "mycoolpassword"
        user_payload = json.dumps({
            "email": email,
            "password": password
        })

        response = self.app.post(
            '/api/auth/signup', 
            headers={"Content-Type": "application/json"}, 
            data=user_payload)
        response = self.app.post(
            '/api/auth/login', 
            headers={"Content-Type": "application/json"}, 
            data=user_payload)
        login_token = response.json['token']

        upload_payload = {
            "state": "Happy",
            "lat": -55,
            "long": 76.5
        }

        response = self.app.post(
            '/api/users/50/uploads',
            headers={"Content-Type": "application/json", "Authorization": f"Bearer {login_token}"},
            data=json.dumps(upload_payload))

        # Then
        self.assertEqual("Unauthorized...", response.json['message'])
        self.assertEqual(404, response.status_code)
