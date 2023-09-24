from flask import make_response, request
from flask_restful import Resource, abort
from flask_jwt_extended import create_access_token

from ..database.models import User

from ..database.db import db

import datetime

class SignupApi(Resource):
    def post(self):
        body = request.get_json()
        if User.query.filter_by(email=body['email']).first() is not None:
            abort(400,  message="User already exists. Please Login...")

        user = User(**body)
        user.hash_password()
        db.session.add(user)
        db.session.commit()
        return make_response({"data": "User has been created..."}, 200)

class LoginApi(Resource):
    def post(self):
        body = request.get_json()
        user = User.query.filter_by(email=body['email']).first()
        authorized = user.check_password(body.get('password'))
        if not authorized:
            abort(401, message="Email or password invalid")

        expires = datetime.timedelta(days=7)

        #Register the token with the User(id)
        access_token = create_access_token(identity=user.id, expires_delta=expires)
        return make_response({"token": access_token}, 200)



