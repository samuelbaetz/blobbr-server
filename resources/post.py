from flask_restful import Resource,reqparse
from models.post import PostModel
from models.user import UserModel
from flask_jwt_extended import jwt_required,get_jwt_identity, current_user
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient, BlobClient
import werkzeug
import uuid
from flask import jsonify
from db import db
post_parser = reqparse.RequestParser()
post_parser.add_argument('content',
        type=str,
        required=True,
        help="Required"
)
post_parser.add_argument('likes', type=int)
post_parser.add_argument('imageurl',
        type=werkzeug.datastructures.FileStorage,
        location='files',
        required=False
)
post_parser.add_argument('feed_id')
post_parser.add_argument('user_id')
post_parser.add_argument('pub_date',
        type=str
)
class Post(Resource):
    @classmethod
    def get(cls,post_id):
        post = PostModel.find_by_id(post_id)
        if not post:
            return {'message': 'Post Not Found'}, 404
        return post.json()
    @jwt_required()
    def delete(cls, post_id):
        post = PostModel.find_by_id(post_id)
        
        if post.user_id != current_user.id:
            return {'message': 'This Action is Unauthorized Bro'}, 401
        post.delete_from_db()
        return {'message': 'Post Deleted'}
    @jwt_required()
    def put(cls, post_id):
        data = post_parser.parse_args()
        post = PostModel.find_by_id(post_id)
        if post.user_id != current_user.id:
            return {'message': 'This Action is Unauthorized Bro'}, 401
        post.content = data['content']
        post.save_to_db()
        return post.json()
class CreatePost(Resource):
    @jwt_required()
    def post(self):
        data = post_parser.parse_args()
        post = PostModel(**data)
        post.save_to_db()
        return {"message": "Post Created."}, 201
    
class Posts(Resource):
    @jwt_required()
    def get(cls):
        return {"posts": [post.json() for post in PostModel.query.all()]}
class CreateImagePost(Resource):
    def post(self):
        data = post_parser.parse_args()
        image_file = data['imageurl']
        blob = BlobClient.from_connection_string(conn_str="DefaultEndpointsProtocol=https;EndpointSuffix=core.windows.net;AccountName=image1689;AccountKey=LSKVztWeg3o9R4ufT6o9FtV4eW776/McWu+jaQWzjjrG4RnH8ztwyERNrVv8XIIHrdVnG4heorual1zOuVhjBg==", container_name="images", blob_name=str(uuid.uuid4().fields[-1])[:5] + ".jpg")
        blob.upload_blob(image_file)
        post = PostModel(data['content'],data['likes'],blob.url, data['pub_date'], data['feed_id'], data['user_id'])
        post.save_to_db()
        return {"message": "Image Post Created."}, 201

# class UserPosts(Resource):
#     def get(self):
#         post = db.session.query(PostModel).join(UserModel, PostModel.user).all()
#         return {"posts": [post.json() for post in post]}
        