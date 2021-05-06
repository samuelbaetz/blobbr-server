from db import db
import uuid
from sqlalchemy.dialects.postgresql import UUID
import datetime
class FeedModel(db.Model):
    __tablename__ = 'feeds'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(80))
    created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    description = db.Column(db.String(300))
    avatarurl = db.Column(db.String(200))
    posts = db.relationship('PostModel', lazy='dynamic')
    def __init__(self,name,created_date,description,avatarurl):
        self.name = name
        self.created_date = created_date
        self.description = description
        self.avatarurl = avatarurl
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    def json(self):
        return {'id': str(self.id), 'name': self.name, 'created_date': str(self.created_date),'description': self.description,'avatarurl':self.avatarurl, 'posts': [post.json() for post in self.posts]}
    @classmethod
    def find_by_name(cls,name):
        return cls.query.filter_by(name=name).first()  