import json

from base_case import BaseCase

class TestCreateUpload(BaseCase):

    def test_create_uploads_response(self):
        # Given
        email = "Robjack@wxample.com"
        password = "mycoolpassword"
        user_payload = json.dumps({
            "email": email,
            "password": password
        })

        response = self.app.post('/api/auth/signup', headers={"Content-Type": "application/json"}, data=user_payload)
        response = self.app.post('/api/auth/login', headers={"Content-Type": "application/json"}, data=user_payload)
        login_token = response.json['token']


        upload_payload = {
            "state": "Happy",
            "lat": -55,
            "long": 76.5
        }
        # When
        response = self.app.post('/api/users/1/uploads',
                                 headers={"Content-Type": "application/json", "Authorization": f"Bearer {login_token}"},
                                 data=json.dumps(upload_payload))

        # Then
        self.assertEqual('Capture has been uploaded...', response.json['data'])
        self.assertEqual(200, response.status_code)

    def test_response_with_invalid_user_id(self):
        # Given
        email = "Robjack@wxample.com"
        password = "mycoolpassword"
        user_payload = json.dumps({
            "email": email,
            "password": password
        })

        response = self.app.post('/api/auth/signup', headers={"Content-Type": "application/json"}, data=user_payload)
        response = self.app.post('/api/auth/login', headers={"Content-Type": "application/json"}, data=user_payload)
        login_token = response.json['token']


        upload_payload = {
            "state": "Happy",
            "lat": -55,
            "long": 76.5
        }
        # When
        response = self.app.post('/api/users/50/uploads',
                                 headers={"Content-Type": "application/json", "Authorization": f"Bearer {login_token}"},
                                 data=json.dumps(upload_payload))

        # Then
        self.assertEqual("Unauthorized...", response.json['message'])
        self.assertEqual(401, response.status_code)