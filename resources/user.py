
from flask_restful import Resource,reqparse
from models.user import UserModel
from models.TokenBlocklist import TokenBlocklist
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import create_access_token, create_refresh_token
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient, BlobClient
from flask_jwt_extended import get_jwt_identity, jwt_required,current_user,get_jwt
from flask import jsonify
import werkzeug
import uuid
from datetime import datetime
from datetime import timedelta
from datetime import timezone
class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
        type=str,
        required=True,
        help="This field is required."    
    )
    parser.add_argument('password',
        type=str,
        required=True,
        help="This field is required."    
    )
    parser.add_argument('email',
        type=str,
        required=True,
        help="This field is required."    
    )
    parser.add_argument('avatarurl', 
        type=werkzeug.datastructures.FileStorage,
        location='files'    
    )
    def post(self):
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {'message': "A user with that username already exists."},400
        image_file = data['avatarurl']
        blob = BlobClient.from_connection_string(conn_str="DefaultEndpointsProtocol=https;EndpointSuffix=core.windows.net;AccountName=image1689;AccountKey=LSKVztWeg3o9R4ufT6o9FtV4eW776/McWu+jaQWzjjrG4RnH8ztwyERNrVv8XIIHrdVnG4heorual1zOuVhjBg==", container_name="images", blob_name=str(uuid.uuid4().fields[-1])[:5] + ".jpg")
        blob.upload_blob(image_file)
        user = UserModel(data['username'], data['password'], data['email'], blob.url)
        user.save_to_db()

        return {"message": "User Created!"}, 201

class User(Resource):
    @classmethod
    @jwt_required()
    def get(cls,user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': 'User Not found'},404
        return user.json()

    @classmethod
    @jwt_required()
    def delete(cls, user_id):
        user = UserModel.find_by_id(user_id)
        
        if current_user.id != user_id:
            return {'message': 'This Action is Unauthorized Bro'}, 401
        user.delete_from_db()
        return {'message': 'User Deleted'}

class UserLogin(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
        type=str,
        required=True,
        help="This field is required."    
    )
    parser.add_argument('password',
        type=str,
        required=True,
        help="This field is required."    
    )
    @classmethod
    def post(cls):
        data = cls.parser.parse_args()

        user = UserModel.find_by_username(data['username'])

        if user and user.verify_password(data['password']):
            access_token = create_access_token(identity=user.id, fresh=True)
            
            return{
                'access_token': access_token,
                'user': [user.json()]
            }
        return {'message': 'Invalid Credentials'}, 401
class Users(Resource):
    @jwt_required()
    def get(cls):
        return {"users": [user.json() for user in UserModel.query.all()]}

class UserProfile(Resource):
    @jwt_required()
    def get(cls):
        current_user = get_jwt_identity()
        return {"user": str(current_user)},200
class UserLogout(Resource):
    @jwt_required()
    def post(self):
        jti = get_jwt()["jti"]
        now = datetime.now(timezone.utc)
        token = TokenBlocklist(jti=jti, created_at=now)
        token.save_to_db()
        return {"message": "Logged Out Successfully!"}