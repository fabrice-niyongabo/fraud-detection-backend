import os
import pandas as pd
import numpy as np
import h2o
from h2o.automl import H2OAutoML
import re
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
import time

# Configuration
DATA_PATH = "dataset/data.csv"
MODEL_DIR = "../model"

def main():
    """Main function to train the SMS threat detection model"""
    print("=" * 50)
    print("SMS THREAT DETECTION MODEL TRAINER")
    print("=" * 50)
    
    # Create model directory if it doesn't exist
    os.makedirs(MODEL_DIR, exist_ok=True)
    
    # Start H2O
    print("\nInitializing H2O...")
    h2o.init()
    
    # Load data
    print(f"\nLoading data from {DATA_PATH}...")
    if not os.path.exists(DATA_PATH):
        print(f"ERROR: Data file not found: {DATA_PATH}")
        return
    
    try:
        df = pd.read_csv(DATA_PATH)
        print(f"Successfully loaded {len(df)} records.")
    except Exception as e:
        print(f"ERROR: Failed to load data: {str(e)}")
        return
    
    # Verify data format
    if 'text' not in df.columns or 'label' not in df.columns:
        print("ERROR: CSV must have 'text' and 'label' columns.")
        return
    
    # Data summary
    print("\nData summary:")
    print(f"Total samples: {len(df)}")
    label_counts = df['label'].value_counts()
    for label, count in label_counts.items():
        print(f"  - {label}: {count} ({count/len(df)*100:.1f}%)")
    
    # Preprocess data
    print("\nPreprocessing text data...")
    df['preprocessed_text'] = df['text'].apply(preprocess_text)
    
    # Feature extraction
    print("Extracting features using TF-IDF...")
    vectorizer = TfidfVectorizer(max_features=5000)
    X = vectorizer.fit_transform(df['preprocessed_text'])
    
    # Encode labels
    label_encoder = LabelEncoder()
    df['label'] = label_encoder.fit_transform(df['label'])
    
    # Convert to H2O frame
    print("Converting to H2O frame...")
    X_df = pd.DataFrame(X.toarray())
    h2o_frame = h2o.H2OFrame(pd.concat([X_df, pd.DataFrame(df['label'], columns=['label'])], axis=1))
    
    # Ensure label is categorical
    h2o_frame['label'] = h2o_frame['label'].asfactor()
    
    # Split data
    train, test = h2o_frame.split_frame(ratios=[0.8])
    
    # Train model
    print("\nTraining model with H2O AutoML...")
    start_time = time.time()
    automl = H2OAutoML(max_models=20, max_runtime_secs=300, seed=42)
    automl.train(x=list(range(X_df.shape[1])), y='label', training_frame=train, validation_frame=test)
    training_time = time.time() - start_time
    
    # Get best model
    best_model = automl.leader
    
    # Print model performance
    print("\nModel training completed!")
    print(f"Training time: {training_time:.2f} seconds")
    
    print("\nBest model performance:")
    print(f"  Model type: {best_model.algo}")
    available_metrics = best_model._model_json['output']['training_metrics']._metric_json.keys()
    print("  Available metrics:", available_metrics)
    
    if 'AUC' in available_metrics:
        print(f"  AUC: {best_model.auc():.4f}")
    else:
        print("  AUC metric is not available for this model.")
    
    print(f"  Accuracy: {best_model.accuracy()[0][1]:.4f}")
    print(f"  Logloss: {best_model.logloss():.4f}")
    
    # Save model components
    print("\nSaving model components...")
    
    # Save vectorizer
    vectorizer_path = os.path.join(MODEL_DIR, 'tfidf_vectorizer.pkl')
    joblib.dump(vectorizer, vectorizer_path)
    print(f"  Saved vectorizer to {vectorizer_path}")
    
    # Save label encoder
    encoder_path = os.path.join(MODEL_DIR, 'label_encoder.pkl')
    joblib.dump(label_encoder, encoder_path)
    print(f"  Saved label encoder to {encoder_path}")
    
    # Save H2O model
    model_path = h2o.save_model(best_model, path=MODEL_DIR)
    print(f"  Saved H2O model to {model_path}")
    
    print("\nModel training and saving complete!")
    print(f"All model components saved to '{MODEL_DIR}' directory")

def preprocess_text(text):
    """Preprocess text for SMS threat detection"""
    text = str(text).lower()
    text = re.sub(r'[^\w\s!?.]', '', text)  # Remove special characters
    text = ' '.join(text.split())  # Remove extra spaces
    return text

if __name__ == "__main__":
    main()
