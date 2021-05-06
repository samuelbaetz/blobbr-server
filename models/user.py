from db import db
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
from sqlalchemy.dialects.postgresql import UUID
user_posts = db.Table('user_posts',
    db.Column('user_id', UUID(as_uuid=True), db.ForeignKey('users.id'), primary_key=True,default=uuid.uuid4),
    db.Column('post_id', UUID(as_uuid=True), db.ForeignKey('posts.id'), primary_key=True,default=uuid.uuid4)
)
user_comments = db.Table('user_comments',
    db.Column('user_id', UUID(as_uuid=True), db.ForeignKey('users.id'), primary_key=True, default=uuid.uuid4),
    db.Column('comment_id', UUID(as_uuid=True), db.ForeignKey('comments.id'), primary_key=True, default=uuid.uuid4)
)
class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(300))
    email = db.Column(db.String(120))
    avatarurl = db.Column(db.String(200))
    posts = db.relationship('PostModel', lazy='dynamic')
    comments = db.relationship('CommentModel', lazy='dynamic')
    def __init__(self,username, password,email,avatarurl):
        self.username = username
        self.password = generate_password_hash(password)
        self.email = email
        self.avatarurl = avatarurl
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    def json(self):
        return {
            'id': str(self.id),
            'username': self.username,
            'email': self.email,
            'avatarurl': self.avatarurl,
            'posts': [post.json() for post in self.posts],
            'comments': [comment.json() for comment in self.comments]
        }
    def userjson(self):
        return {
            'id': str(self.id),
            'username': self.username,
            'email': self.email,
            'avatarurl': self.avatarurl,
            
        }
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()
    def verify_password(self,pwd):
        return check_password_hash(self.password,pwd)   

