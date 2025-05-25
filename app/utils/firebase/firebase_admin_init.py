import firebase_admin
from firebase_admin import credentials

# Load the service account key JSON file
cred = credentials.Certificate("serviceAccount.json")

# Initialize the Firebase app
firebase_app = firebase_admin.initialize_app(cred)