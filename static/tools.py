import firebase_admin 
from firebase_admin import credentials, firestore
import random as rand


cred = credentials.Certificate("static/key.json")
firebase_admin.initialize_app(cred)
# type of intelligence: {question: answer}

db = firestore.client()

def generate_random_id():
    return rand.randint(1, 99999)
    

def upload(val):
    id = generate_random_id()
    db.collection('intell').document(str(id)).set(val)
