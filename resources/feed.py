from flask_restful import Resource,reqparse
from models.feed import FeedModel
from flask_jwt_extended import jwt_required,get_jwt_identity, current_user
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient, BlobClient
import werkzeug
import uuid
feed_parser = reqparse.RequestParser()
feed_parser.add_argument('name',
        type=str,
        required=True,
        help="Required"
)
feed_parser.add_argument('created_date',
        type=str
)
feed_parser.add_argument('description', type=str)
feed_parser.add_argument('avatarurl',
        type=werkzeug.datastructures.FileStorage,
        location='files',
        required=False
)
class Feed(Resource):
    def get(self,name):
        feed = FeedModel.find_by_name(name)
        if feed:
            return feed.json()
        return {"message": "Feed Not Found"}, 404
class Feeds(Resource):
    def get(cls):
        return {"feeds": [feed.json() for feed in FeedModel.query.all()]}

class CreateFeed(Resource):
    def post(self):
        data = feed_parser.parse_args()
        image_file = data['avatarurl']
        blob = BlobClient.from_connection_string(conn_str="DefaultEndpointsProtocol=https;EndpointSuffix=core.windows.net;AccountName=image1689;AccountKey=LSKVztWeg3o9R4ufT6o9FtV4eW776/McWu+jaQWzjjrG4RnH8ztwyERNrVv8XIIHrdVnG4heorual1zOuVhjBg==", container_name="images", blob_name=str(uuid.uuid4().fields[-1])[:5] + ".jpg")
        blob.upload_blob(image_file)
        feed = FeedModel(data['name'], data['created_date'], data['description'], blob.url)
        feed.save_to_db()
        return {"message": "Feed Created"}, 201