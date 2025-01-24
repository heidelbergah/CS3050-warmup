import sys
import json

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate("firestore_private_key.json")
firebase_admin.initialize_app(cred)



