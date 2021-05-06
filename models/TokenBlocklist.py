from db import db

class TokenBlocklist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    def __init__(self,jti, created_at):
        self.jti = jti
        self.created_at = created_at
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
