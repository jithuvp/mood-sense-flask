
# MoodSense App

## Description
The camera on your shiny new phone can sense a user’s mood based on their facial features, where
mood can be characterized as either happy, sad or neutral to start with. 

This application leverages the phone’s mood-sensing
capability to collect mood data and provide insights:
* Upload a mood capture for a given user and location
* Return the mood frequency distribution for a given user
* Return the proximity to locations (home, office, shopping center,...) where a given user is
happy.

## Technology Stack
* Python 3.9.10
* Flask RESTful
* SQLite
* Pandas
* Geopy

## Features
Current:
* JSON Web Token Authentication 
* Add/View/Edit/Delete User Information
* Upload mood characteristics and location
* Delete an upload
* View mood frequency distribution of a user
* View proximity to locations where user is happy

To-Do:
* Pagination on the REST API
* Password Reset option
* URLs (HATEOAS)

## Installation

The libraries are available on PyPI, and can be installed with pip:
```shell
pip install -r requirements.txt
```
(The requirements.txt file is located in the root dir)

### Initialize the environment variables

* Update the variables inside the `.env` file
  * Note: The value of `JWT_SECRET_KEY` can be anything
* The `ENV_FILE_LOCATION` is the environment variable which should store the location of .env file relative to app.py
  * To set this value, run the command: `export ENV_FILE_LOCATION=./.env`

## Data Model and Persistence 

The application uses a SQLite database to store data. The data is stored in 3 tables:
* `users_user`
  * fields: 
  ```json 
        id: int
    first_name: str
    last_name: str
    email: str
    password: str
    created: datetime
    last_updated: datetime
  ```
* `users_uploads`
  * fields:
  ```json
    id:int
    state:str
    user_id:int
    created: datetime
  ```
* `uploads_location`
  * fields:
  ```json
    id: int
    lat: float
    long: float
    type: str
    upload_id: int
  ```

##Usage: REST API
###Endpoints
* `/api/auth/signup` 
* `/api/auth/login`
* `/api/users/me`
* `/api/users/<user_id>`
* `/api/users/<user_id>/uploads`
* `/api/users/<user_id>/states`
* `/api/users/<user_id>/proximity`

An example of a general workflow:
1. User signs up via `/api/auth/signup`
2. User logs in using the same email/password via `/api/auth/login`
3. User sends a GET request to `/api/users/me` to get the `id`
4. User uploads capture information using `api/users/<user_id>/uploads`
5. User can GET analysis of their uploads via `/api/users/<user_id>/states` and/or `users/<user_id>/proximity`

### Authentication

#### Login
API clients authenticate with the app, which generates an access token that must be included as a header in all subsequent API requests.

`POST /api/auth/login`

**Parameters**:
* Headers:
  * Content-Type: `application/json`
* Body
  * `email` (Required)
  * `password`(Required)
    
#### Example:

Request:
```shell
curl --location --request POST 'http://localhost:5000/api/auth/login' \
--header 'Content-Type: application/json' \
--data-raw '{
    "email": "JohnDale123@example.com",
    "password": "my_password"
}'
```
Response:
* status code : `200`
```json
{
    "token": <token_string>
}
```

### SignUp/ Create User
Allows for creating a profile for a new user. The passwords are encrypted
on the fly using `flask-bcrypt`

`POST /api/auth/signup`

Parameters:
* Headers:
  * Content-Type: `application/json`
* Body
  * `email` (Required)
  * `password`(Required)
  * `first_name` (Optional)
  * `last_name` (Optional)
    
#### Example:

Request:
```shell
curl --location --request POST 'http://localhost:5000/api/auth/signup' \
--header 'Content-Type: application/json' \
--data-raw '{
    "email": "JohnDale123@example.com",
    "password": "my_password"
}'
```
Response:
* status code : `200`
```json
{
    "data": "User has been created..."
}
```

### View user profile
The user context is set based on the access token so that the user (after logging in) can navigate to `users/me` to view their 
user profile. 

**Note**: Alternatively, the user can access their profile via `users/<user_id>`

`GET /api/api/users/me`

Parameters:
* Headers:
  * Authorization: Bearer token
    
####Example:

Request:
```shell
curl --location --request GET 'http://localhost:5000/api/users/me' \
--header 'Authorization: Bearer <token_string>'
```
Response:
* status code : `200`
```json
{
    "created": "Mon, 21 Mar 2022 14:22:31 GMT",
    "email": "JohnDale123@example.com",
    "first_name": null,
    "id": 7,
    "last_name": null,
    "last_updated": null,
    "password": "$2b$12$85dhKWyNzr2rJAUbLlswHOtXb2Q6nPmsQU9C09WHkVGXA.ASCOPM2"
}
```


### Update user information

`PATCH /api/api/users/<user_id>`

Parameters:
* Headers:
  * Content-Type: `application/json`
  * Authorization: Bearer token
* Body
  * `first_name`
  * `last_name`
  * `email`
  * `password`
    
#### Example:

Request:
```shell
curl --location --request PATCH 'http://localhost:5000/api/users/7' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer <token_string>' \
--data-raw '{
    "first_name": "John", 
    "last_name": "Dale Smith"
}'
```
Response:
* status code : `200`
```json
{
    "created": "Mon, 21 Mar 2022 14:22:31 GMT",
    "email": "JohnDale123@example.com",
    "first_name": "John",
    "id": 7,
    "last_name": "Dale Smith",
    "last_updated": "Mon, 21 Mar 2022 18:36:26 GMT",
    "password": "$2b$12$85dhKWyNzr2rJAUbLlswHOtXb2Q6nPmsQU9C09WHkVGXA.ASCOPM2"
}
```

### Upload Capture Features
User can upload the mood state/characteristics:`['happy', 'neutral', 'sad']` along with location (GPS)
coordinates. Every `POST` request will add a new row in the database.

`POST api/users/<user_id>/uploads`

Parameters:
* Headers:
  * Content-Type: `application/json`
  * Authorization: Bearer token
  
* Body:
  * `state` - mood state (required)
  * `lat` - latitude (required)
  * `long` - longitude (required)
    
#### Example:

Request:
```shell
curl --location --request POST 'http://localhost:5000/api/users/7/uploads' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer <token_string>' \
--data-raw '{
    "state": "happy", 
    "lat": 37.75850848099701,
    "long": -122.50833008408812
}'
```
Response:
* status code : `200`
```json
{
    "data": "Capture has been uploaded..."
}
```

### View Uploads
Allows to view all uploads of a given user.

`GET api/users/<user_id>/uploads`

Parameters:
* `<user_id>`
* Headers:
  * Authorization: Bearer token
    
#### Example:

Request:
```shell
curl --location --request GET 'http://localhost:5000/api/users/7/uploads' \
--header 'Authorization: Bearer <token_string>'
```
Response:
* status code : `200`
```json
[
    {
        "id": 6,
        "location": {
            "lat": 37.75850848099701,
            "long": -122.50833008408812,
            "type": "Supermarket"
        },
        "state": "happy",
        "user_id": 7
    }
]
```
### Delete Uploads

`DELETE api/users/<user_id>/uploads`

Parameters:
* `<user_id>`
* Headers:
  * Content-Type: `application/json`
  * Authorization: Bearer token

* Body:
  * `id` - upload id  (required)
    
#### Example:

Request:
```shell
curl --location --request DELETE 'http://localhost:5000/api/users/7/uploads' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer <token_string>' \
--data-raw '{
    "id": 6
}'
```
Response:
* status code : `204` (NO CONTENT)

### View Frequency Distribution of User States 

User can obtain a frequency distribution of their mood characteristic or states

`GET api/users/<user_id>/states`

Parameters:
* `<user_id>`
* Headers:

  * Authorization: Bearer token
    
### Example:

Request:
```shell
curl --location --request GET 'http://localhost:5000/api/users/7/states' \
--header 'Authorization: Bearer <token_string>'
```
Response:
* status code : `200`
```json
{
    "data": [
        {
            "proportion_percent": 66.6666666667,
            "state": "happy"
        },
        {
            "proportion_percent": 33.3333333333,
            "state": "neutral"
        }
    ]
}
```
### View Proximity  
User can find proximity (in kms) to location where the user was happy previously.

`GET api/users/<user_id>/proximity`

Parameters:
* `<user_id>`
* Headers:
  * Authorization: Bearer token
    
#### Example:

Request:
```shell
curl --location --request GET 'http://localhost:5000/api/users/7/proximity' \
--header 'Authorization: Bearer <token_string>'
```
Response:
* status code : `200`
```json
{
    "data": [
        {
            "distance_to_in_kms": 12473.5685276232,
            "type": "Work"
        },
        {
            "distance_to_in_kms": 12856.4779509774,
            "type": "Supermarket"
        }
    ]
}
```



