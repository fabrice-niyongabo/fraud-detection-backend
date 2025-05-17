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
        # check if message already exists
        msg = Message.query.filter_by(
            _id=_id,
            userId=userId,
            address=address,
            date=date
        ).first()
        if msg:
            raise ValueError(f"Message already analyzed")
        
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
    
def getUserMessages(userId):
    try:
        messages = Message.query.filter_by(userId=userId).all()
        return [msg.toJSON() for msg in messages]
    except Exception as e: 
        raise Exception(f"{str(e)}")
    
 