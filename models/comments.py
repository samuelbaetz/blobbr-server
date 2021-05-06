from db import db
import uuid
from sqlalchemy.dialects.postgresql import UUID
import datetime
from models.user import UserModel, user_comments
class CommentModel(db.Model):
    __tablename__ = 'comments'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    content = db.Column(db.String(280))
    likes = db.Column(db.Integer, default=0)
    created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    post_id = db.Column(UUID(as_uuid=True), db.ForeignKey('posts.id'),default=uuid.uuid4)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'),default=uuid.uuid4)
    post = db.relationship('PostModel')
    user = db.relationship('UserModel',secondary=user_comments, backref=db.backref('users', lazy='dynamic'), lazy='dynamic')
    def __init__(self,content,likes,created_date,post_id, user_id):
        self.content = content
        self.likes = likes
        self.created_date = created_date
        self.post_id = post_id
        self.user_id = user_id
    def json(self):
        return {
            "id": str(self.id),
            "content": self.content,
            "likes": self.likes,
            "created_date": str(self.created_date),
            "post_id": str(self.post_id),
            "user_id": str(self.user_id),
            "user": [user.userjson() for user in self.user]
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
    def find_by_id(cls,_id):
        return cls.query.filter_by(id=_id).first()