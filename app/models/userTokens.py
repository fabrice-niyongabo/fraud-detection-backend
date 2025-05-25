import re
from datetime import datetime,timezone
from app.extensions import db 


class UserToken(db.Model):
    __tablename__ = 'user_tokens'
     
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, nullable=False)
    token = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    
    def __repr__(self):
        return f'<UserToken {self.userId}>'
    
    # Serialize the user object =>  converting it to json
    def toJSON(self):
        return {
            "id": self.id,
            "userId": self.userId,
            "token": self.token,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    