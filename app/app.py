#import the framework
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

from flask_restful import Api
from .resources.routes import initialize_routes #remove --app.-- in local

from .database.db import initialize_db

#create an instance of Flask
app = Flask(__name__)
app.config.from_envvar('ENV_FILE_LOCATION')

api = Api(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)


initialize_db(app)
initialize_routes(api)


