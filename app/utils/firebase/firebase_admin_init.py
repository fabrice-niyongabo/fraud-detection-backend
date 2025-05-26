import os

import firebase_admin
from firebase_admin import credentials

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
cred_path = os.path.join(BASE_DIR, "serviceAccount.json")

# Load the service account key JSON file
cred = credentials.Certificate(cred_path)

# Initialize the Firebase app
firebase_app = firebase_admin.initialize_app(cred)