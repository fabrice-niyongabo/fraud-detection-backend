from flask import Flask, jsonify, request   
from http import HTTPStatus
import logging
from app.utils import auth
from app.services import userService,messageService
from app.utils import prediction,asyncTask



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
            result = threat_detection_model.predict(message)
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
            msg = messageService.saveMessage(
                message=message,
                address=address,
                userId=userId,
                _id=_id,
                date=date
            )
            asyncTask.processSMS.delay(message,msg['id'])
            return {'message': "Message processed successfully"}, HTTPStatus.OK
        except Exception as e:
            return {'message': str(e)}, HTTPStatus.INTERNAL_SERVER_ERROR