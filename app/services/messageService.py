from app.models.messages import Message
from app.extensions import db

def saveMessage(
        message: str,
        address: str,
        userId: int,
        _id: str,
        date:str
    ):
    try:
        newMessage = Message(
            message = message,
            address = address,
            userId = userId,
            _id = _id,
            date = date
        )
        
        # Add the new data to the session and commit
        db.session.add(newMessage)
        db.session.commit()
        
        return newMessage.toJSON()
    except Exception as e:
        db.session.rollback() 
        raise Exception(f"{str(e)}")