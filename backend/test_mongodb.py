import os
import django
import json

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rainwater_harvester.settings')
django.setup()

from rainwater_harvester.api.database import get_mongodb_status

def test_mongodb_connection():
    status = get_mongodb_status()
    print("MongoDB Connection Status:")
    print(json.dumps(status, indent=2))

if __name__ == "__main__":
    test_mongodb_connection()
