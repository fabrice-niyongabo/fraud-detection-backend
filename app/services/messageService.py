from app.models.messages import Message
from app.extensions import db

def saveMessage(
        message: str,
        translated_message: str,
        address: str,
        userId: int,
        _id: str,
        date:str
    ):
    try:
        newMessage = Message(
            message = message,
            translated_message = translated_message,
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

def updateMessagePrediction(
        id,
        prediction
    ):
    try:
        msg = Message.query.get(id)
        if not msg:
            raise ValueError("Message not found")
        msg.prediction = prediction
        db.session.commit()
        
        return msg.toJSON()
    except Exception as e:
        db.session.rollback() 
        raise Exception(f"{str(e)}")
 