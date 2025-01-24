import os
from google.cloud import firestore

def parse_query(input_query):
    parts = input_query.split(' ')

    