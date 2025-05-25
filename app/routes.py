from flask import Flask, jsonify, request   
from http import HTTPStatus
import logging 
from app.services import userService,messageService,notificationService
from app.utils import auth, prediction, translation



# Initialize model
threat_detection_model = prediction.SMSThreatDetectionModel()

def register_routes(app: Flask) -> None: 
    @app.route("/")
    def index():
         return {"message":"Running..."}, HTTPStatus.OK
    
    @app.route("/api/login", methods=['POST'])
    def login():
        try:
            data = request.get_json()
            email = data.get('email')
            password = data.get('password')
            token, user = userService.login(email=email,password=password)
            
            return {"token": token, "user":user, "user_type":"user"}, HTTPStatus.OK
        except Exception as e:
            return {"message":str(e)}, HTTPStatus.BAD_REQUEST
        
    @app.route("/api/register", methods=['POST'])
    def register():
        try:
            data = request.get_json()
            email = data.get('email')
            password = data.get('password')
            names = data.get('names')
            user = userService.register(password=password,email=email,names=names)
            
            return {"user":user}, HTTPStatus.OK
        except ValueError as e:
            return {"message":str(e)}, HTTPStatus.BAD_REQUEST
        except Exception as e:
            return {"message":str(e)}, HTTPStatus.INTERNAL_SERVER_ERROR
        
    @app.route('/api/detect', methods=['POST'])
    def detect_threat():
        try:
            message = request.json['message']
            translated_message = translation.translate(message)
            result = threat_detection_model.predict(translated_message)
            return {'result': result}, HTTPStatus.OK
        except Exception as e:
            return {'message': str(e)}, HTTPStatus.INTERNAL_SERVER_ERROR
    
    @app.route('/api/analyse', methods=['POST'])
    @auth.token_required
    def analyseSMS(current_user):
        try:
            message = request.json['body']
            date = request.json['date']
            _id = request.json['_id']
            address = request.json['address']
            userId = current_user['id']
            
            translated_message = translation.translate(message)
            msg = messageService.saveMessage(
                message=message,
                translated_message=translated_message,
                address=address,
                userId=userId,
                _id=_id,
                date=date
            )
            print("Message:", message)
            print("message translated:", translated_message)
            result = threat_detection_model.predict(translated_message)
            messageService.updateMessagePrediction(msg['id'],result['threat_probability'])
            
            # Notification
            try:
                if result['threat_probability'] > 0.5:
                    notificationService.send_notification_to_user(userId,"Message detected as fraudulent")
            except Exception as e:
                logging.exception("Error sending notification")
            return {'message': "Message processed successfully"}, HTTPStatus.OK
        except Exception as e:
            print(e)
            return {'message': str(e)}, HTTPStatus.INTERNAL_SERVER_ERROR
        
    @app.route('/api/messages/mine')
    @auth.token_required
    def getMyMessages(current_user):
        try:
            userId = current_user['id']
            messages = messageService.getUserMessages(userId)
            return {'messages': messages}, HTTPStatus.OK
        except Exception as e:
            logging.error(e)
            return {'message': str(e)}, HTTPStatus.INTERNAL_SERVER_ERROR
    
    @app.route('/api/messages/mine', methods=['PUT'])
    @auth.token_required
    def reportMessage(current_user):
        try:
            userId = current_user['id']
            data = request.get_json()
            id = data.get('id')
            comment = data.get('comment')
            messageService.handleMessageReport(id,userId,comment)
            return {'message': "Message has been reported!"}, HTTPStatus.OK
        except Exception as e:
            logging.error(e)
            return {'message': str(e)}, HTTPStatus.INTERNAL_SERVER_ERROR
    
    @app.route('/api/messages/mine/<int:id>', methods=['DELETE'])
    @auth.token_required
    def deleteMessage(current_user,id):
        try:
            userId = current_user['id']
            messageService.deleteMessage(id,userId)
            return {'message': "Message has been deleted!"}, HTTPStatus.OK
        except Exception as e:
            logging.error(e)
            return {'message': str(e)}, HTTPStatus.INTERNAL_SERVER_ERROR
        
    @app.route('/api/profile/names', methods=['PUT'])
    @auth.token_required
    def updateUserNames(current_user):
        try:
            userId = current_user['id']
            data = request.get_json()
            names = data.get('names')
            userService.updateUserNames(userId,names)
            return {'message': "Names updated successfully"}, HTTPStatus.OK
        except Exception as e:
            logging.error(e)
            return {'message': str(e)}, HTTPStatus.INTERNAL_SERVER_ERROR
        
    @app.route('/api/profile/password', methods=['PUT'])
    @auth.token_required
    def updateUserPassword(current_user):
        try:
            userId = current_user['id']
            data = request.get_json()
            newPassword = data.get('newPassword')
            oldPassword = data.get('oldPassword')
            userService.updatedPassword(userId,newPassword,oldPassword)
            return {'message': "Password updated successfully"}, HTTPStatus.OK
        except Exception as e:
            logging.error(e)    
            return {'message': str(e)}, HTTPStatus.INTERNAL_SERVER_ERROR
        
    @app.route('/api/token', methods=['POST'])
    @auth.token_required
    def saveUserToken(current_user):
        try:
            userId = current_user['id']
            data = request.get_json() 
            token = data.get('token')
            userService.saveUserToken(userId,token)
            return {'message': "Token saved successfully"}, HTTPStatus.OK  
        except Exception as e:
            logging.error(e)    
            return {'message': str(e)}, HTTPStatus.INTERNAL_SERVER_ERROR
        