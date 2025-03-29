import os
import pandas as pd
import h2o 
import re
import joblib

class SMSThreatDetectionModel:
    def __init__(self):
        # Initialize H2O
        h2o.init()
        
        # Paths for saving/loading model components
        base_dir = os.path.dirname(os.path.dirname(__file__))
        self.model_path = os.path.join(base_dir,'model', 'sms_threat_detection_model')
        self.vectorizer_path = os.path.join(base_dir,'model', 'tfidf_vectorizer.pkl')
        self.label_encoder_path = os.path.join(base_dir,'model', 'label_encoder.pkl')
        
        
    def preprocess_text(self, text):
        """
        Preprocess SMS text for feature extraction
        """
        # Convert to lowercase
        text = str(text).lower()
        
        # Remove special characters and numbers
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        
        # Remove extra whitespaces
        text = ' '.join(text.split())
        
        return text 
    
    def predict(self, message):
        """
        Predict if a message is a threat
        """
        # Load saved components
        vectorizer = joblib.load(self.vectorizer_path)
        label_encoder = joblib.load(self.label_encoder_path)
        
        # Preprocess message
        preprocessed_message = self.preprocess_text(message)
        
        # Vectorize message
        X = vectorizer.transform([preprocessed_message])
        
        # Convert to H2O frame
        h2o_frame = h2o.H2OFrame(pd.DataFrame(X.toarray()))
        
        # Load saved model
        model = h2o.load_model(self.model_path)
        
        # Predict
        prediction = model.predict(h2o_frame)
        predicted_label = prediction['predict'][0][0]
        predicted_prob = prediction['predict_proba'][0][1]
        
        # Decode label
        label = label_encoder.inverse_transform([int(predicted_label)])[0]
        
        return {
            'threat_probability': float(predicted_prob),
            'is_threat': label == 'threat',
            'label': label
        }