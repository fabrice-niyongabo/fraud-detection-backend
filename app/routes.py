from flask import Flask, jsonify, request   
from http import HTTPStatus
import logging
from app.utils import auth
from app.services import userService
import json

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