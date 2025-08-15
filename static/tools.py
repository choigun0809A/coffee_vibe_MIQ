import firebase_admin 
import os, json
from firebase_admin import credentials, firestore
import random as rand

key_dict = json.loads(os.environ['/etc/secrets/KEY'])
cred = credentials.Certificate(key_dict)
firebase_admin.initialize_app(cred)
# type of intelligence: {question: answer}

db = firestore.client()

def generate_random_id():
    return rand.randint(1, 99999)
    

def upload(val):
    id = generate_random_id()
    db.collection('intell').document(str(id)).set(val)


# def get_users():
#     """Retrieve all documents from the 'intell' collection as a list."""
#     users_ref = db.collection('intell')
#     docs = users_ref.stream()
    
#     # Convert documents to a list of dictionaries
#     users_list = []
#     for doc in docs:
#         print(doc)
#         user_data = doc.to_dict()
#         user_data['id'] = doc.id  # Include document ID
#         users_list.append(user_data)
    
#     return users_list

# get_users()
