from pymongo import MongoClient
import os
from dotenv import load_dotenv
from bson.objectid import ObjectId

load_dotenv()


def get_mongo_client():
    client = MongoClient(os.getenv('MONGODB_URI'))
    return client


def store_document_data(document_data):
    client = get_mongo_client()
    db = client['document_database']
    collection = db['document_collection']
    result = collection.insert_one(document_data)
    return result.inserted_id


def get_document_by_id(document_id):
    client = get_mongo_client()
    db = client['document_database']
    collection = db['document_collection']
    document = collection.find_one({'_id': ObjectId(document_id)})
    if document:
        document['_id'] = str(document['_id'])  # Convert ObjectId to string for JSON serialization
    return document
