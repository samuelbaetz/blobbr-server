from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from db import db
from models.user import UserModel
from resources.user import UserRegister, User,UserLogin,Users,UserProfile, UserLogout
from models.feed import FeedModel
from models.post import PostModel
from resources.feed import Feed,Feeds,CreateFeed
from resources.post import Post, CreatePost, Posts, CreateImagePost
from models.comments import CommentModel
from resources.comments import CreateComment, Comment
from models.TokenBlocklist import TokenBlocklist
from flask_cors import CORS
app = Flask(__name__)

CORS(app,resources={r"/*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:root@localhost:5432/blobbbr"
api = Api(app)
db.init_app(app)
migrate = Migrate(app,db)
app.secret_key = "jlkjou00i0i0f039409i30jkf"
jwt = JWTManager(app)
app.config['PROPAGATE_EXCEPTIONS'] = True

@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return UserModel.query.filter_by(id=identity).one_or_none()
@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]
    token = db.session.query(TokenBlocklist.id).filter_by(jti=jti).scalar()
    return token is not None
api.add_resource(UserRegister, '/register')
api.add_resource(User, '/users/<string:user_id>')
api.add_resource(UserLogin, '/login')
api.add_resource(Feed, '/feed/<string:name>')
api.add_resource(Feeds, '/feeds')
api.add_resource(CreateFeed,'/createfeed')
api.add_resource(Post, '/posts/<string:post_id>')
api.add_resource(CreatePost, '/createpost')
api.add_resource(Posts, '/posts')
api.add_resource(Users, '/users')
api.add_resource(CreateImagePost, '/createimagepost')
api.add_resource(UserProfile, '/profile')
api.add_resource(CreateComment, '/createcomment')
api.add_resource(Comment, '/comment/<string:comment_id>')
api.add_resource(UserLogout, '/logout')

if __name__ == '__main__':
    app.run(host='172.22.20.179', port=5006, debug=True) 