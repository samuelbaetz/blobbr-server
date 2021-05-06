from db import db
import uuid
from sqlalchemy.dialects.postgresql import UUID
import datetime
from models.user import UserModel, user_posts
class PostModel(db.Model):
    __tablename__ = 'posts'
     
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    content = db.Column(db.String(280))
    likes = db.Column(db.Integer, default=0)
    imageurl = db.Column(db.String(300))
    pub_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    feed_id = db.Column(UUID(as_uuid=True), db.ForeignKey('feeds.id'),default=uuid.uuid4)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'),default=uuid.uuid4)
    feed = db.relationship('FeedModel')
    user = db.relationship('UserModel',secondary=user_posts, backref=db.backref('user', lazy='dynamic'), lazy='dynamic')
    comments = db.relationship('CommentModel', lazy='dynamic')

    def __init__(self,content,likes,imageurl,pub_date,feed_id,user_id):
        self.content = content
        self.likes = likes
        self.imageurl = imageurl
        self.pub_date = pub_date
        self.feed_id = feed_id
        self.user_id = user_id

    def json(self):
        return {
            'id': str(self.id),
            'content': self.content,
            'likes': self.likes,
            'pub_date': str(self.pub_date),
            'imageurl': self.imageurl,
            'feed_id': str(self.feed_id),
            'user_id': str(self.user_id),
            'comments': [comment.json() for comment in self.comments],
            'user': [user.userjson() for user in self.user]
        }
    def save_to_db(self):
        User = UserModel.query.filter_by(id=self.user_id).first()
        self.user.append(User)
        db.session.add(self)
        db.session.commit()
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
    @classmethod
    def find_by_id(cls, _id):
        return cls.query.join(UserModel).filter_by(id=_id).first()  
    
