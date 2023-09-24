from flask import jsonify, make_response, request
from flask_restful import Resource, abort
from flask_jwt_extended import jwt_required, get_jwt_identity

from ..database.models import User, Location, Upload
from ..models_objects import LocationSchema, UploadsSchema

from ..database.db import db

from .locationmapper import location_type_selector
from .process_states import get_freq_dist
from .analyze_proximity import check_proximity


class UsersApi(Resource):
    @jwt_required()
    def get(self):
        
        try:
            token_user_id = get_jwt_identity()
        except Exception as e:
            # Handle the invalid token error here
            abort(401, message="Invalid token")
        result = User.query.filter_by(id=token_user_id).first()
        return make_response(jsonify(result), 200)

class UsersByIdApi(Resource):
    @jwt_required()
    def get(self, user_id):
        
        try:
            token_user_id = get_jwt_identity()
        except Exception as e:
            # Handle the invalid token error here
            abort(401, message="Invalid token")
        if token_user_id != user_id:
            abort(404, message="Unauthorized or not found...")

        result = User.query.filter_by(id=user_id).first()
        return make_response(jsonify(result), 200)

    @jwt_required()
    def patch(self, user_id):
        
        try:
            token_user_id = get_jwt_identity()
        except Exception as e:
            # Handle the invalid token error here
            abort(401, message="Invalid token")
        if token_user_id != user_id:
            abort(404, message="Unauthorized or not found...")

        body = request.get_json()
        db.session.query(User).filter_by(id=user_id).update(body)

        db.session.commit()
        result = db.session.query(User).filter_by(id=user_id).first()
        return make_response(jsonify(result), 200)

    @jwt_required()
    def delete(self, user_id):
        
        try:
            token_user_id = get_jwt_identity()
        except Exception as e:
            # Handle the invalid token error here
            abort(401, message="Invalid token")
        if token_user_id != user_id:
            abort(404, message="Unauthorized...")

        user = User.query.get(user_id)
        db.session.delete(user)
        db.session.commit()
        return make_response({}, 204)

class UploadsApi(Resource):
    @jwt_required()
    def get(self, user_id):
        
        try:
            token_user_id = get_jwt_identity()
        except Exception as e:
            # Handle the invalid token error here
            abort(401, message="Invalid token")
        if token_user_id != user_id:
            abort(404, message="Unauthorized...")
        result = UploadsSchema(many=True).dump(Upload.query.filter_by(user_id=user_id).all())
        if not result:
            abort(404, message="Uploads is empty...")
        return make_response(jsonify(result), 200)

    @jwt_required()
    def post(self, user_id):

        try:
            token_user_id = get_jwt_identity()
        except Exception as e:
            # Handle the invalid token error here
            abort(401, message="Invalid token")
        if token_user_id != user_id:
            abort(404, message="Unauthorized...")
        body = request.get_json()

        required_fields = ['state', 'lat', 'long']
    
        for field in required_fields:
            if field not in body:
                abort(400, message=f"Missing argument '{field}' in the body...")

        # Convert 'state' to lowercase
        body['state'] = body['state'].lower()
        # obtain location characteristics
        body['type'] = location_type_selector(body['lat'], body['long'])

        upload = Upload(state=body['state'], user_id=token_user_id)
        db.session.add(upload)
        db.session.flush()
        location = Location(lat=body['lat'], long=body['long'], type=body['type'], upload_id=upload.id)
        db.session.add(location)
        db.session.commit()
        return make_response({"data": "Capture has been uploaded..."}, 201)

    @jwt_required()
    def delete(self, user_id):
        body = request.get_json()
        try:
            token_user_id = get_jwt_identity()
        except Exception as e:
            # Handle the invalid token error here
            abort(401, message="Invalid token")

        if token_user_id != user_id:
            abort(404, message="Unauthorized...")

        if 'id' not in body:
            abort(404, message="missing argument 'id' in the body...")

        upload = Upload.query.get(body['id'])
        if not upload:
            abort(404, message="Invalid upload Id...")
        db.session.delete(upload)
        db.session.commit()
        return make_response({}, 204)

class StatesApi(Resource):
    @jwt_required()
    def get(self, user_id):
        try:
            token_user_id = get_jwt_identity()
        except Exception as e:
            # Handle the invalid token error here
            abort(401, message="Invalid token")
        result = UploadsSchema(many=True).dump(Upload.query.filter_by(user_id=user_id).all())
        if not result:
            abort(404, message="No uploads yet...")

        processed_result = get_freq_dist(result)
        return make_response({"data": processed_result})


class ProximityApi(Resource):
    @jwt_required()
    def get(self, user_id):
        try:
            token_user_id = get_jwt_identity()
        except Exception as e:
            # Handle the invalid token error here
            abort(401, message="Invalid token")
        #token_user_id = get_jwt_identity()
        result = UploadsSchema(many=True).dump(Upload.query.filter_by(user_id=user_id).all())
        
        if not result:
            abort(404, message="No uploads yet...")

        '''
        The current location is assumed to be the GPS 
        coordinates from the most recent upload/capture
        '''
        current_location = db.session.query(
            Location.lat, Location.long
        ).join(
            Upload, Location.upload_id == Upload.id
        ).filter(
            Upload.user_id == user_id
        ).order_by(
            Location.id.desc()
        ).first()

        #obtain calculated distance
        processed_result = check_proximity(result, current_location)
        print(processed_result)

        return make_response({"data": processed_result})