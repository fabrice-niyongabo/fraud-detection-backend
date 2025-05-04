import re
from datetime import datetime,timezone
from sqlalchemy.orm import validates
from app.extensions import db 


class Message(db.Model):
    __tablename__ = 'messages'
     
    id = db.Column(db.Integer, primary_key=True)
    _id = db.Column(db.String(128), nullable=False)
    date = db.Column(db.String(128), nullable=False)
    address = db.Column(db.String(120),nullable=False)
    message = db.Column(db.Text, nullable=True)
    prediction = db.Column(db.DECIMAL(10,2),default=0.0, nullable=True)
    userId = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    
    def __repr__(self):
        return f'<Message {self.id}>'
    
    # Serialize the user object =>  converting it to json
    def toJSON(self):
        return {
            "id": self.id,
            "_id": self._id,
            "date": self.date,
            "address": self.address,
            "message": self.message,
            "prediction": self.prediction,
            "userId": self.userId,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }