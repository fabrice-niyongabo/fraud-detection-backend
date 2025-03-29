
from flask import Flask 
# from app.extensions import db, migrate, redis_client
from app.extensions import db, migrate
from app.config import Config
from flask_cors import CORS

def create_app(config_class=Config):
    app = Flask(__name__) 
    CORS(app) # enable CORS
    app.config.from_object(config_class) 
    
    db.init_app(app) 
    migrate.init_app(app, db)
    # redis_client.init_app(app)
    
    with app.app_context(): 
        # Create tables for our models
        from app import models
        db.create_all()

    return app
