from app.models.users import User
from app.extensions import db
import jwt
import bcrypt
from datetime import datetime, timedelta 
from app.config import Config
# from app.schemas import UserSchema


def register(
        names: str, 
        email: str,
        password: str, 
    ):
    try:
        params = {
            "names": names, 
            "email": email,
            "password": password, 
        }

        # Check if any required parameter is empty
        for param_name, param_value in params.items():
            if not param_value:
                raise ValueError(f"'{param_name}' is required and cannot be empty.")
        
        # Validate pwd
        if len(params["password"]) < 5:
            raise ValueError("Password must be greater or equal to 5 characters long.")

        hashedPassword = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        newUser = User(
            names = names,
            password = hashedPassword,
            email = email
        )
        
        # Add the new data to the session and commit
        db.session.add(newUser)
        db.session.commit()
        
        return newUser.toJSON()
    
    except ValueError as e:
        db.session.rollback() 
        raise ValueError(f"{str(e)}")
    
    except Exception as e:
        db.session.rollback() 
        raise Exception(f"{str(e)}")

def login(
        email:str,
        password:str,
    ):
    try:
        if not email or not password:
            raise ValueError("Invalid login information")
        
        user = User.query.filter_by(email=email).first() 
        if not user:
           raise ValueError("Wrong email or password")
         
        if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            raise ValueError("Wrong email or password")
        
        token = jwt.encode({
            "id": user.id, 
            "email": user.email,
            "names": user.names,
            'exp': datetime.utcnow() + timedelta(days=365)  # Token expiry time
        }, Config.JWT_SECRET_KEY)
        
        userJSON = user.toJSON()
        return token, userJSON
            
    except ValueError as e: 
        raise ValueError(f"{str(e)}")
    
    except Exception as e: 
        raise Exception(f"{str(e)}")
    
def updateUserNames(userId,names):
    try:
        user = User.query.get(userId)
        if not user:
            raise ValueError("User not found")
        user.names = names
        db.session.commit()
        return user.toJSON()
    except Exception as e:
        db.session.rollback()
        raise Exception(f"{str(e)}")
    
def updatedPassword(userId,newPassword,oldPassword):
    try:
        user = User.query.get(userId)
        if not user:
            raise ValueError("User not found")
        if not bcrypt.checkpw(oldPassword.encode('utf-8'), user.password.encode('utf-8')):
            raise ValueError("Wrong old password")
        
        hashedPassword = bcrypt.hashpw(newPassword.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        user.password = hashedPassword
        db.session.commit()
        return user.toJSON()
    except Exception as e:
        db.session.rollback()
        raise Exception(f"{str(e)}")