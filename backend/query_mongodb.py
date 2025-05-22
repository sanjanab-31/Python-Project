import os
import django
from datetime import datetime, timedelta
from bson import ObjectId
import json

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rainwater_harvester.settings')
django.setup()

from django.conf import settings
from pymongo import MongoClient

class MongoJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)

def print_results(title, results):
    print(f"\n=== {title} ===")
    print(json.dumps(list(results), indent=2, cls=MongoJSONEncoder))

def main():
    # Connect to MongoDB
    client = MongoClient(settings.MONGODB_URI)
    db = client[settings.MONGODB_NAME]
    
    # 1. Find all leaking tanks
    print_results("Leaking Tanks", 
        db.historical_data.find({"isLeaking": True}).limit(3)
    )
    
    # 2. Find tanks with high water usage (drinking > 45%)
    print_results("High Drinking Water Usage", 
        db.historical_data.find({"waterUsage.drinking": {"$gt": 45}}).limit(3)
    )
    
    # 3. Find tanks in Chennai with capacity > 3000
    print_results("Large Tanks in Chennai",
        db.historical_data.find({
            "location": "Chennai",
            "tankCapacity": {"$gt": 3000}
        }).limit(3)
    )
    
    # 4. Find tanks with low water level (< 30% of capacity)
    print_results("Low Water Level Tanks",
        db.historical_data.find({
            "$expr": {
                "$lt": [
                    {"$divide": ["$currentLevel", "$tankCapacity"]},
                    0.3
                ]
            }
        }).limit(3)
    )
    
    # 5. Find average rainfall by location
    pipeline = [
        {"$group": {
            "_id": "$location",
            "avgRainfall": {"$avg": "$rainfall"},
            "totalRecords": {"$sum": 1}
        }},
        {"$sort": {"avgRainfall": -1}}
    ]
    print_results("Average Rainfall by Location",
        db.historical_data.aggregate(pipeline)
    )
    
    # 6. Find water efficiency (inflow vs outflow) by location
    pipeline = [
        {"$group": {
            "_id": "$location",
            "avgInflow": {"$avg": "$inflow"},
            "avgOutflow": {"$avg": "$outflow"},
            "efficiency": {
                "$avg": {
                    "$divide": ["$inflow", "$outflow"]
                }
            }
        }},
        {"$sort": {"efficiency": -1}}
    ]
    print_results("Water Efficiency by Location",
        db.historical_data.aggregate(pipeline)
    )

if __name__ == "__main__":
    main()
