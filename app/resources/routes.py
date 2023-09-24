from .mood import UsersApi,UsersByIdApi, UploadsApi, StatesApi, ProximityApi
from .auth import SignupApi, LoginApi

def initialize_routes(api):
    api.add_resource(SignupApi, '/api/auth/signup')
    api.add_resource(LoginApi, '/api/auth/login')
    api.add_resource(UsersApi, "/api/users/me")
    api.add_resource(UsersByIdApi, "/api/users/<int:user_id>")
    api.add_resource(UploadsApi, "/api/users/<int:user_id>/uploads")
    api.add_resource(StatesApi, "/api/users/<int:user_id>/states")
    api.add_resource(ProximityApi, "/api/users/<int:user_id>/proximity")

