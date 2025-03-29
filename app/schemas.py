# Helps us to convert data (incase of a list) from our models 
# directly to JSON without making much configurations(looping through them, etc)
# => converting a list to JSON direcly.
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from app.models.users import User
from app.models.admins import Admin

class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        include_relationships = True  # Include relationships if any
        
class AdminSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Admin
        include_relationships = True  # Include relationships if any

