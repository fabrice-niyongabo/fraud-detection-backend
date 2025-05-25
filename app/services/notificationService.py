 
from app.models.userTokens import UserToken
from app.extensions import db
from firebase_admin import messaging, exceptions
from app.utils.firebase.firebase_admin_init import firebase_admin
import logging

def send_notification_to_user(title: str, body: str, token: str, data: dict = {}) -> None:
    try:
        message = messaging.Message(
            token=token,
            notification=messaging.Notification(
                title=title,
                body=body
            ),
            data={**data, "title": title, "body": body}
        )

        response = messaging.send(message)
        print("Successfully sent Firebase notification:", response)
    except exceptions.FirebaseError as error:
        print("Failed to send Firebase notification", error)
        if getattr(error, 'code', '') == "messaging/registration-token-not-registered":
            remove_invalid_token(token)

def send_notification_to_multiple_users(registration_tokens: list[str], title: str, body: str, data: dict = {}) -> list[dict] | Exception:
    sent = []
    try:
        for token in registration_tokens:
            try:
                send_notification_to_user(title, body, token, data)
                sent.append({"token": token})
            except Exception as error:
                logging.exception("Error sending to token %s", token)
                if getattr(error, 'code', '') == "messaging/registration-token-not-registered":
                    remove_invalid_token(token)
        return sent
    except Exception as e:
        logging.exception("Error while sending notifications to multiple users")
        return e

def remove_invalid_token(token: str) -> None:
    try:
        token_record = UserToken.query.filter_by(token=token).first()
        if token_record:
            db.session.delete(token_record)
            db.session.commit()
            print("FB token deleted!", token)
    except Exception as e:
        logging.exception("Failed to delete invalid token")


def send_notification_to_user(userId: int, message: str) -> None:
    try:
        tokenList = []
        user_tokens = UserToken.query.filter_by(userId=userId).all()
        if not user_tokens:
            raise ValueError("No user tokens found for user")
        for token in user_tokens:
            tokenList.append(token.token)
            
        send_notification_to_multiple_users(tokenList, "Fraud Message Detected!", message, {"message": message})
    except Exception as e:
        logging.exception("Failed to send notification to user")