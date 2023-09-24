import json

from base_case import BaseCase

class TestUpdateUser(BaseCase):

    def test_update_user_response(self):
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


        update_user_payload = {
            "first_name": "Rob",
            "last_name": "Jack",
        }
        response = self.app.patch('/api/users/1',
                                 headers={"Content-Type": "application/json", "Authorization": f"Bearer {login_token}"},
                                 data=json.dumps(update_payload))

        # When
        response = self.app.get('/api/users/1')
        added_user = response.json[0]

        # Then
        self.assertEqual(update_user_payload['first_name'], added_user['first_name'])
        self.assertEqual(update_user_payload['last_name'], added_user['last_name'])
        self.assertEqual(update_user_payload['email'], added_user['email'])
        self.assertEqual(200, response.status_code)

    def test_response_with_invalid_id(self):
        def test_user_response(self):
            # Given
            email = "Robjack@wxample.com"
            password = "mycoolpassword"
            user_payload = json.dumps({
                "email": email,
                "password": password
            })

            response = self.app.post('/api/auth/signup', headers={"Content-Type": "application/json"},
                                     data=user_payload)
            response = self.app.post('/api/auth/login', headers={"Content-Type": "application/json"}, data=user_payload)
            login_token = response.json['token']

            update_user_payload = {
                "first_name": "Rob",
                "last_name": "Jack",
            }
            response = self.app.patch('/api/users/1',
                                      headers={"Content-Type": "application/json",
                                               "Authorization": f"Bearer {login_token}"},
                                      data=json.dumps(update_payload))
