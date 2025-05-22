import os
import django
from pymongo import MongoClient
from bson import ObjectId
import json

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rainwater_harvester.settings')
django.setup()

from django.conf import settings

# MongoDB JSON encoder
class MongoJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        return super().default(obj)

def print_collection(collection, name):
    print(f"\n=== {name} ===")
    documents = list(collection.find())
    if documents:
        print(json.dumps(documents, indent=2, cls=MongoJSONEncoder))
    else:
        print("No documents found")
    print(f"Total documents: {len(documents)}")

def main():
    # Connect to MongoDB
    client = MongoClient(settings.MONGODB_URI)
    db = client[settings.MONGODB_NAME]
    
    print(f"Connected to database: {settings.MONGODB_NAME}")
    
    # List all collections
    collections = db.list_collection_names()
    print("\nCollections in database:")
    for collection in collections:
        print(f"- {collection}")
    
    # View data in each collection
    print_collection(db.user_inputs, "User Inputs")
    print_collection(db.calculation_results, "Calculation Results")
    print_collection(db.historical_data, "Historical Data")
    print_collection(db.user_settings, "User Settings")

if __name__ == "__main__":
    main()
