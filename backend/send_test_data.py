import os
import django
from datetime import datetime, timedelta
import random

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rainwater_harvester.settings')
django.setup()

from rainwater_harvester.api.database import (
    save_user_input,
    save_calculation_results,
    save_historical_data,
    save_user_settings
)

def generate_test_data():
    # List of test locations
    locations = ["Chennai", "Bangalore", "Mumbai", "Delhi", "Hyderabad"]
    
    print("=== Sending Test Data to MongoDB ===\n")

    # 1. Generate User Inputs
    print("1. Generating User Inputs...")
    for location in locations:
        input_data = {
            'roofArea': random.randint(80, 200),
            'tankCapacity': random.randint(1000, 6000),
            'location': location,
            'timestamp': datetime.now().isoformat()
        }
        result = save_user_input(input_data)
        print(f"Added input for {location}: {result}")

    # 2. Generate Historical Data
    print("\n2. Generating Historical Data...")
    for i in range(7):  # Last 7 days of data
        for location in locations:
            historical_data = {
                'timestamp': (datetime.now() - timedelta(days=i)).isoformat(),
                'location': location,
                'roofArea': random.randint(80, 200),
                'tankCapacity': random.randint(1000, 6000),
                'inflow': random.uniform(50, 200),
                'outflow': random.uniform(100, 300),
                'rainfall': round(random.uniform(0.5, 3.0), 2),
                'currentLevel': random.uniform(1000, 4000),
                'waterUsage': {
                    'drinking': random.randint(30, 50),
                    'cleaning': random.randint(30, 50),
                    'gardening': random.randint(10, 30)
                },
                'isLeaking': random.choice([True, False])
            }
            result = save_historical_data(historical_data)
            print(f"Added historical data for {location} on day -{i}: {result.get('_id') if result else 'Failed'}")

    # 3. Generate Calculation Results
    print("\n3. Generating Calculation Results...")
    latest_input = {
        'roofArea': 150,
        'tankCapacity': 5000,
        'location': 'Chennai'
    }
    input_result = save_user_input(latest_input)
    
    if input_result:
        calculation = {
            'waterCollected': random.uniform(1000, 3000),
            'efficiency': random.uniform(0.7, 0.95),
            'recommendations': [
                'Clean gutters monthly',
                'Install water level sensor',
                'Consider expanding storage capacity'
            ],
            'predictions': {
                'nextWeek': random.uniform(500, 1500),
                'nextMonth': random.uniform(2000, 4000)
            }
        }
        result = save_calculation_results(calculation)
        print(f"Added calculation result: {result.get('_id') if result else 'Failed'}")

    # 4. Update User Settings
    print("\n4. Updating User Settings...")
    settings = {
        'defaultRoofArea': 150,
        'defaultTankCapacity': 5000,
        'alertThreshold': 0.2,
        'notifications': True,
        'preferences': {
            'dailyUpdates': True,
            'alertsEnabled': True,
            'measurementUnit': 'metric'
        }
    }
    result = save_user_settings(settings)
    print(f"Updated settings: {result.get('_id') if result else 'Failed'}")

if __name__ == "__main__":
    generate_test_data()
