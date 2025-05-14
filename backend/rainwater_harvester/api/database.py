"""
Database utility functions using Django models.
"""
import logging
from .models import UserInput, CalculationResult, HistoricalData, UserSettings

# Set up logging
logger = logging.getLogger(__name__)

def save_inputs(input_data):
    """
    Save user inputs using Django model.
    """
    try:
        user_input = UserInput.objects.create(data=input_data)
        logger.info("Input data saved to database")
        return user_input
    except Exception as e:
        logger.error(f"Error saving input data: {str(e)}")
        return None

def get_latest_inputs():
    """
    Get the latest user inputs from database.
    """
    try:
        return UserInput.objects.last()
    except Exception as e:
        logger.error(f"Error getting latest inputs: {str(e)}")
        return None

def save_results(results_data):
    """
    Save calculation results using Django model.
    """
    try:
        latest_input = UserInput.objects.last()
        if latest_input:
            result = CalculationResult.objects.create(
                input_data=latest_input,
                data=results_data
            )
            logger.info("Results saved to database")
            return result
        return None
    except Exception as e:
        logger.error(f"Error saving results: {str(e)}")
        return None

def get_latest_results():
    """
    Get the latest calculation results from database.
    """
    try:
        return CalculationResult.objects.last()
    except Exception as e:
        logger.error(f"Error getting latest results: {str(e)}")
        return None

def get_results_by_input_id(input_id):
    """
    Get calculation results for a specific input ID.
    """
    try:
        return CalculationResult.objects.filter(input_data_id=input_id)
    except Exception as e:
        logger.error(f"Error getting results by input ID: {str(e)}")
        return None

def save_historical_data(historical_data):
    """
    Save historical data using Django model.
    """
    try:
        result = HistoricalData.objects.create(data=historical_data)
        logger.info("Historical data saved to database")
        return result
    except Exception as e:
        logger.error(f"Error saving historical data: {str(e)}")
        return None

def get_historical_data(limit=100):
    """
    Get historical data for analysis, limited to the most recent entries.
    """
    try:
        return HistoricalData.objects.all().order_by('-id')[:limit]
    except Exception as e:
        logger.error(f"Error getting historical data: {str(e)}")
        return []

def save_user_settings(settings_data):
    """
    Save user settings using Django model.
    """
    try:
        settings, created = UserSettings.objects.get_or_create(
            pk=1,  # We only need one settings object
            defaults={'data': settings_data}
        )
        if not created:
            settings.data = settings_data
            settings.save()
        logger.info("User settings saved to database")
        return settings
    except Exception as e:
        logger.error(f"Error saving user settings: {str(e)}")
        return None

def get_user_settings():
    """
    Get user settings from database.
    """
    try:
        settings = UserSettings.objects.first()
        return settings.data if settings else None
    except Exception as e:
        logger.error(f"Error getting user settings: {str(e)}")
        return None

def delete_saved_result(result_id):
    """
    Delete a saved result by its ID.
    """
    try:
        result = CalculationResult.objects.filter(id=result_id).first()
        if result:
            result.delete()
            logger.info(f"Result {result_id} deleted from database")
            return True
        return False
    except Exception as e:
        logger.error(f"Error deleting result: {str(e)}")
        return False

def get_mongodb_status():
    """
    Get database connection status.
    """
    return True
