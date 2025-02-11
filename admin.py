import sys
import json
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

"""
IMPORTANT:
    The "firestore_private_key.json" should not be uploaded to
    the github. Make sure you have a local copy of the key
    in this directory and you'll be good to go :)

INSTRUCTIONS:
    Run the command `python3 admin.py cereal.json` and the code
    will do the rest. You might need to use `python` instead of
    `python3` depending on your computer.

    Most important rule: have fun B)
"""


def establish_connection():
    """
    Establishes a connection to the Firestore database if not already done using the provided service account key.

    Returns:
        firestore.client: A Firestore client object to interact with the database.
    """
    if not firebase_admin._apps:  # Check if Firebase is already initialized
        cred = credentials.Certificate("firestore_private_key.json")
        firebase_admin.initialize_app(cred)
    return firestore.client()


def parse_json_data(json_file):
    """
    Reads and parses data from a JSON file.

    Args:
        json_file: The path to the JSON file.

    Returns:
        The parsed JSON data, or None if an error occurs.
    """
    try:
        with open(json_file, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error reading JSON file: {e}")
        return None


def push_data(db, data, collection_name):
    """
    Uploads data to a specified Firestore collection.

    Args:
        db: The Firestore client object.
        data: The data to upload.
        collection_name: The name of the Firestore collection.
    """
    for item in data:
        db.collection(collection_name).add(item)


def collection_exists(db, collection_name):
    """
    Checks if a Firestore collection exists by querying for at least one document.

    Args:
        db: The Firestore client object.
        collection_name: The name of the Firestore collection.

    Returns:
        True if the collection exists (has at least one document), False otherwise.
    """
    docs = db.collection(collection_name).limit(1).get()
    return len(docs) > 0


def delete_collection(db, collection_name):
    """
    Deletes all documents in a Firestore collection.

    Args:
        db: The Firestore client object.
        collection_name: The name of the Firestore collection.
    """
    prior_collection = db.collection(collection_name)
    docs = prior_collection.limit(1).get()

    while len(docs) > 0:
        for doc in docs:
            doc.reference.delete()
        docs = prior_collection.limit(1).get()


def initialize_database(collection_name="cereal_data"):
    """
    Initializes the database by reading JSON data, checking for an existing collection,
    deleting it if it exists, and uploading new data.

    Args:
        collection_name: The name of the Firestore collection (default: "cereal_data").
    """
    if len(sys.argv) < 2:
        print("No JSON argument provided; Please provide a JSON file")
        return

    json_file = sys.argv[1]
    data = parse_json_data(json_file)

    if data is None:
        return


    db = establish_connection()
    
    if collection_exists(db, collection_name):
        delete_collection(db, collection_name)
    
    push_data(db, data, collection_name)
    print("Data pushed to database successfully!")


if __name__ == "__main__":
    initialize_database()

