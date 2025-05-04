from celery import Celery

celery_app = Celery(
    'my_app',
    broker='redis://default:ASp4AAIjcDEzM2Q3YjkwZWNiZDQ0YzgzYmVhYmEzMWRjNGZkNzg4MHAxMA@inspired-mule-10872.upstash.io:6379',
    # backend='redis://localhost:6379/0'  # Optional
)

@celery_app.task
def processSMS(message,id):
    from app.utils import prediction
    from app.models.messages import Message
    from app.extensions import db
    threat_detection_model = prediction.SMSThreatDetectionModel()
    result = threat_detection_model.predict(message)
    
    # Update the prediction column in the database
    db.session.query(Message).filter_by(id=id).update({'prediction': round(result['threat_probability'],2)})
    db.session.commit()