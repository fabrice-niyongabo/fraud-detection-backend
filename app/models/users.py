import re
from datetime import datetime,timezone
from sqlalchemy.orm import validates
from app.extensions import db 


class User(db.Model):
    __tablename__ = 'users'
     
    id = db.Column(db.Integer, primary_key=True)
    names = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phoneNumber = db.Column(db.String(10), nullable=True)
    password = db.Column(db.Text,  nullable=False)
    type = db.Column(db.String(10), default="user",  nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    
    def __repr__(self):
        return f'<User {self.email}>'
    
    # Serialize the user object =>  converting it to json
    def toJSON(self):
        return {
            "id": self.id,
            "names": self.names,
            "email": self.email,
            "type": self.type,
            "phoneNumber": self.phoneNumber,
            "password": self.password,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    # validate email address
    @validates('email')
    def validate_email(self, key, address):
        if not re.match(r'[^@]+@[^@]+\.[^@]+', address):
            raise ValueError(f"Invalid email address: {address}")
        return address