import os
import django
import json
from datetime import datetime
from bson import ObjectId

class MongoJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        return super().default(obj)

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rainwater_harvester.settings')
django.setup()

from rainwater_harvester.api.database import (
    get_mongodb_status,
    save_user_input,
    get_latest_inputs,
    save_calculation_results,
    get_latest_results,
    save_historical_data,
    get_historical_data,
    save_user_settings,
    get_user_settings,
    delete_saved_result
)

def test_all_operations():
    print("\n=== Testing MongoDB Operations ===\n")

    # 1. Test MongoDB Connection
    print("1. Testing MongoDB Connection...")
    status = get_mongodb_status()
    print(json.dumps(status, indent=2, cls=MongoJSONEncoder))

    if status.get('status') != 'connected':
        print("MongoDB is not connected. Please check your connection and try again.")
        return

    # 2. Test User Input Operations
    print("\n2. Testing User Input Operations...")
    test_input = {
        'roofArea': 100,
        'tankCapacity': 1000,
        'location': 'New York',
        'timestamp': datetime.now().isoformat()
    }
    saved_input = save_user_input(test_input)
    print("Saved Input:", json.dumps(saved_input, indent=2, cls=MongoJSONEncoder))

    latest_input = get_latest_inputs()
    print("Latest Input:", json.dumps(latest_input, indent=2, cls=MongoJSONEncoder))

    # 3. Test Calculation Results
    print("\n3. Testing Calculation Results...")
    test_result = {
        'waterCollected': 500,
        'efficiency': 0.85,
        'recommendations': ['Clean gutters', 'Check tank seals']
    }
    saved_result = save_calculation_results(test_result)
    print("Saved Result:", json.dumps(saved_result, indent=2, cls=MongoJSONEncoder))

    latest_result = get_latest_results()
    print("Latest Result:", json.dumps(latest_result, indent=2, cls=MongoJSONEncoder))

    # 4. Test Historical Data
    print("\n4. Testing Historical Data...")
    test_historical = {
        'date': datetime.now().isoformat(),
        'rainfall': 25.4,
        'waterLevel': 750
    }
    saved_historical = save_historical_data(test_historical)
    print("Saved Historical Data:", json.dumps(saved_historical, indent=2, cls=MongoJSONEncoder))

    historical_data = get_historical_data(limit=5)
    print("Recent Historical Data:", json.dumps(historical_data, indent=2, cls=MongoJSONEncoder))

    # 5. Test User Settings
    print("\n5. Testing User Settings...")
    test_settings = {
        'defaultRoofArea': 100,
        'defaultTankCapacity': 1000,
        'alertThreshold': 0.2,
        'notifications': True
    }
    saved_settings = save_user_settings(test_settings)
    print("Saved Settings:", json.dumps(saved_settings, indent=2, cls=MongoJSONEncoder))

    current_settings = get_user_settings()
    print("Current Settings:", json.dumps(current_settings, indent=2, cls=MongoJSONEncoder))

    # 6. Test Delete Operation
    if saved_result:
        print("\n6. Testing Delete Operation...")
        result_id = saved_result.get('_id')
        deleted = delete_saved_result(result_id)
        print(f"Delete Result: {'Success' if deleted else 'Failed'}")

if __name__ == "__main__":
    test_all_operations()
