"""
Database utility functions using Django models.
"""
import logging
from datetime import datetime
from django.conf import settings
from pymongo import MongoClient
from django.apps import apps

# Get model classes
UserInput = apps.get_model('api', 'UserInput')
CalculationResult = apps.get_model('api', 'CalculationResult')
HistoricalData = apps.get_model('api', 'HistoricalData')
UserSettings = apps.get_model('api', 'UserSettings')

# Set up MongoDB connection
client = MongoClient(settings.MONGODB_URI)
db = client[settings.MONGODB_NAME]

# Set up logging
logger = logging.getLogger(__name__)

def save_user_input(input_data):
    """
    Save user inputs to MongoDB.
    """
    try:
        # Add timestamp if not present
        if 'timestamp' not in input_data:
            input_data['timestamp'] = datetime.now().isoformat()

        # Save to MongoDB
        result = db.user_inputs.insert_one(input_data)
        logger.info(f"Input data saved to MongoDB with ID: {result.inserted_id}")
        
        # Return the saved document
        return db.user_inputs.find_one({'_id': result.inserted_id})
    except Exception as e:
        logger.error(f"Error saving input data to MongoDB: {str(e)}")
        return None

def get_latest_inputs():
    """
    Get the latest user inputs from MongoDB.
    """
    try:
        # Get the most recent input by timestamp
        return db.user_inputs.find_one(
            sort=[('timestamp', -1)]
        )
    except Exception as e:
        logger.error(f"Error getting latest inputs from MongoDB: {str(e)}")
        return None

def save_calculation_results(results_data):
    """
    Save calculation results to MongoDB.
    """
    try:
        # Get the latest input
        latest_input = get_latest_inputs()
        
        if latest_input:
            # Prepare the calculation result document
            result_doc = {
                'timestamp': datetime.now().isoformat(),
                'input_data': latest_input,
                'data': results_data
            }
            
            # Save to MongoDB
            result = db.calculation_results.insert_one(result_doc)
            logger.info(f"Calculation results saved to MongoDB with ID: {result.inserted_id}")
            
            # Return the saved document
            return db.calculation_results.find_one({'_id': result.inserted_id})
        return None
    except Exception as e:
        logger.error(f"Error saving calculation results to MongoDB: {str(e)}")
        return None

def get_latest_results():
    """
    Get the latest calculation results from MongoDB.
    """
    try:
        # Get the most recent result by timestamp
        return db.calculation_results.find_one(
            sort=[('timestamp', -1)]
        )
    except Exception as e:
        logger.error(f"Error getting latest results from MongoDB: {str(e)}")
        return None

def get_results_by_input_id(input_id):
    """
    Get calculation results for a specific input ID.
    """
    try:
        return db.calculation_results.find({'input_data._id': input_id})
    except Exception as e:
        logger.error(f"Error getting results by input ID: {str(e)}")
        return None

def save_historical_data(historical_data):
    """
    Save historical data to MongoDB.
    """
    try:
        # Add timestamp if not present
        if 'timestamp' not in historical_data:
            historical_data['timestamp'] = datetime.now().isoformat()
            
        # Save to MongoDB
        result = db.historical_data.insert_one(historical_data)
        logger.info(f"Historical data saved to MongoDB with ID: {result.inserted_id}")
        
        # Return the saved document
        return db.historical_data.find_one({'_id': result.inserted_id})
    except Exception as e:
        logger.error(f"Error saving historical data to MongoDB: {str(e)}")
        return None

def get_historical_data(limit=100):
    """
    Get historical data from MongoDB, limited to the most recent entries.
    """
    try:
        # Get the most recent entries by timestamp
        cursor = db.historical_data.find().sort('timestamp', -1).limit(limit)
        return list(cursor)
    except Exception as e:
        logger.error(f"Error getting historical data from MongoDB: {str(e)}")
        return []

def save_user_settings(settings_data):
    """
    Save user settings to MongoDB.
    """
    try:
        # Add timestamp
        settings_data['last_updated'] = datetime.now().isoformat()
        
        # Update or insert settings document
        result = db.user_settings.update_one(
            {'_id': 'default'},  # We only need one settings document
            {'$set': settings_data},
            upsert=True
        )
        
        logger.info(f"Settings saved to MongoDB")
        
        # Return the updated settings
        return db.user_settings.find_one({'_id': 'default'})
    except Exception as e:
        logger.error(f"Error saving settings to MongoDB: {str(e)}")
        return None

def get_user_settings():
    """
    Get user settings from MongoDB.
    """
    try:
        settings = db.user_settings.find_one({'_id': 'default'})
        return settings if settings else None
    except Exception as e:
        logger.error(f"Error getting user settings from MongoDB: {str(e)}")
        return None

def delete_saved_result(result_id):
    """
    Delete a saved result by its ID from MongoDB.
    """
    try:
        # Try to delete from calculation results
        result = db.calculation_results.delete_one({'_id': result_id})
        if result.deleted_count > 0:
            logger.info(f"Result {result_id} deleted from calculation_results")
            return True
            
        # If not found in calculation results, try historical data
        result = db.historical_data.delete_one({'_id': result_id})
        if result.deleted_count > 0:
            logger.info(f"Result {result_id} deleted from historical_data")
            return True
            
        logger.warning(f"No result found with ID: {result_id}")
        return False
    except Exception as e:
        logger.error(f"Error deleting result from MongoDB: {str(e)}")
        return False

def get_mongodb_status():
    """
    Check MongoDB connection status.
    """
    try:
        # Try to ping the database
        client.admin.command('ping')
        return {
            'status': 'connected',
            'database': settings.MONGODB_NAME,
            'host': settings.MONGODB_URI
        }
    except Exception as e:
        logger.error(f"MongoDB connection error: {str(e)}")
        return {
            'status': 'disconnected',
            'error': str(e)
        }

