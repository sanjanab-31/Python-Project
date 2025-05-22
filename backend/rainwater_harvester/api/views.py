"""
Views for the rainwater harvester API.
"""
from datetime import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import json
import logging
from pymongo import MongoClient
from django.conf import settings
from .serializers import InputSerializer, SettingsSerializer, ResultIdSerializer
from .calculation_service import process_inputs
from .weather_service import get_weather_forecast

# MongoDB setup
client = MongoClient(settings.MONGODB_URI)
db = client[settings.MONGODB_NAME]

# MongoDB collections
user_inputs = db['user_inputs']
calculation_results = db['calculation_results']
historical_data = db['historical_data']
user_settings = db['user_settings']

# Set up logging
logger = logging.getLogger(__name__)

class InputsView(APIView):
    """
    API view for handling user inputs and calculations.
    """
    def post(self, request):
        """
        Process user inputs and return calculation results.
        """
        logger.info(f"Received input request with data: {request.data}")
        serializer = InputSerializer(data=request.data)
        
        if serializer.is_valid():
            try:
                # Add timestamp to input data
                input_data = serializer.validated_data
                input_data['timestamp'] = datetime.now().isoformat()
                
                logger.info(f"Validated input data: {input_data}")
                
                # Save inputs to database using MongoDB directly
                result = db.user_inputs.insert_one(input_data)
                input_id = str(result.inserted_id)
                logger.info(f"Input data saved to database with ID: {input_id}")
                
                # Add input ID to input data
                input_data['_id'] = input_id
                
                # Process inputs and get results
                results = process_inputs(input_data)
                
                # Add input ID to results
                results['input_id'] = input_id
                
                # Save results using MongoDB directly
                result_doc = {
                    'timestamp': datetime.now().isoformat(),
                    'input_data': input_data,
                    'data': results
                }
                result = db.calculation_results.insert_one(result_doc)
                logger.info(f"Results saved to database with ID: {result.inserted_id}")
                
                return Response(results, status=status.HTTP_200_OK)
            except Exception as e:
                logger.error(f"Error processing inputs: {str(e)}", exc_info=True)
                return Response(
                    {
                        'error': 'An error occurred while processing your data.',
                        'details': str(e),
                        'message': 'This could be due to a database connection issue or an error in the calculation service. Please check your database connection and try again.'
                    }, 
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        else:
            logger.error(f"Invalid input data: {serializer.errors}")
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ResultsView(APIView):
    """
    API view for retrieving calculation results.
    """
    def get(self, request):
        """
        Get the latest calculation results.
        """
        try:
            user_input_id = request.query_params.get('user_input_id', None)
            
            if user_input_id:
                logger.info(f"Fetching results for user_input_id: {user_input_id}")
                result = db.calculation_results.find_one({'input_data._id': user_input_id})
                if result:
                    return Response(result['data'], status=status.HTTP_200_OK)
                else:
                    return Response({'message': 'No results found for the given input ID'}, status=status.HTTP_404_NOT_FOUND)
            else:
                logger.info("Fetching latest results")
                result = db.calculation_results.find_one(sort=[('timestamp', -1)])
                if result:
                    return Response(result['data'], status=status.HTTP_200_OK)
                else:
                    return Response({'message': 'No results found'}, status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            logger.error(f"Error retrieving results: {str(e)}")
            return Response(
                {
                    'error': 'An error occurred while retrieving results.',
                    'details': str(e),
                    'message': 'This could be due to a database connection issue. Please check your database connection and try again.'
                }, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class SaveResultsView(APIView):
    """
    API view for saving calculation results to historical data.
    """
    def post(self, request):
        """
        Save calculation results to historical data.
        """
        try:
            # Validate request data
            if not request.data:
                return Response(
                    {
                        'message': 'No data provided',
                        'details': 'Request body is empty'
                    }, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            data = request.data
            
            # Extract key data for historical analysis
            historical_entry = {
                'timestamp': datetime.now().isoformat(),
                'location': data.get('location', ''),
                'inflow': float(data.get('inflow', 0)),
                'outflow': float(data.get('outflow', 0)),
                'tankCapacity': float(data.get('tankCapacity', 0)),
                'waterUsage': data.get('waterUsage', {}),
                'roi': data.get('roi', {}),
                'leakDetection': data.get('leakDetection', {}),
                'maintenanceSchedule': data.get('maintenanceSchedule', []),
                'weatherData': data.get('weatherData', {})
            }
            
            # Validate required fields
            required_fields = ['location', 'inflow', 'outflow', 'tankCapacity']
            missing_fields = [field for field in required_fields if not historical_entry.get(field)]
            
            if missing_fields:
                return Response(
                    {
                        'message': f'Missing required fields: {missing_fields}',
                        'details': 'Please provide all required fields',
                        'required_fields': required_fields
                    }, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Save to MongoDB
            result = historical_data.insert_one(historical_entry)
            logger.info(f"Results saved to historical data with ID: {result.inserted_id}")
            
            # Return saved document
            saved_doc = historical_data.find_one({'_id': result.inserted_id})
            if saved_doc:
                saved_doc['_id'] = str(saved_doc['_id'])  # Convert ObjectId to string
            
            return Response(
                {
                    'message': 'Results saved successfully',
                    'data': saved_doc
                }, 
                status=status.HTTP_201_CREATED
            )
        
        except ValueError as e:
            logger.error(f"Invalid numeric value: {str(e)}")
            return Response(
                {
                    'error': 'Invalid numeric value.',
                    'details': str(e),
                    'message': 'Please ensure all numeric fields contain valid numbers.'
                }, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        except Exception as e:
            logger.error(f"Error saving results: {str(e)}")
            return Response(
                {
                    'error': 'An error occurred while saving results.',
                    'details': str(e),
                    'message': 'This could be due to a database connection issue. Please check your database connection and try again.'
                }, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class HistoricalDataView(APIView):
    """
    API view for retrieving and managing historical data.
    """
    def get(self, request):
        """
        Get historical data for analysis.
        """
        try:
            # Get historical data from database
            data = list(historical_data.find().sort('timestamp', -1))
            # Convert ObjectId to string for JSON serialization
            for item in data:
                item['_id'] = str(item['_id'])
            return Response(data, status=status.HTTP_200_OK)
        
        except Exception as e:
            logger.error(f"Error retrieving historical data: {str(e)}")
            return Response(
                {
                    'error': 'An error occurred while retrieving historical data.',
                    'details': str(e),
                    'message': 'This could be due to a database connection issue. Please check your database connection and try again.'
                }, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            
    def delete(self, request, result_id=None):
        """
        Delete a specific historical data entry.
        """
        try:
            if not result_id:
                return Response(
                    {'message': 'Result ID is required'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
                
            # Delete the result from MongoDB
            from bson.objectid import ObjectId
            result = historical_data.delete_one({'_id': ObjectId(result_id)})
            
            if result.deleted_count > 0:
                return Response(
                    {'message': 'Result deleted successfully'}, 
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {'message': 'Result not found'}, 
                    status=status.HTTP_404_NOT_FOUND
                )
                
        except Exception as e:
            logger.error(f"Error deleting historical data: {str(e)}")
            return Response(
                {
                    'error': 'An error occurred while deleting the result.',
                    'details': str(e),
                    'message': 'This could be due to a database connection issue. Please check your database connection and try again.'
                }, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class SettingsView(APIView):
    """
    API view for managing user settings.
    """
    def get(self, request):
        """
        Get user settings.
        """
        try:
            # Get settings from database
            settings = user_settings.find_one()
            if settings:
                return Response(settings, status=status.HTTP_200_OK)
            else:
                return Response({"message": "No settings found"}, status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            logger.error(f"Error retrieving settings: {str(e)}")
            return Response(
                {
                    'error': 'An error occurred while retrieving settings.',
                    'details': str(e),
                    'message': 'This could be due to a database connection issue. Please check your database connection and try again.'
                }, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def put(self, request):
        """
        Update user settings.
        """
        serializer = SettingsSerializer(data=request.data)
        
        if serializer.is_valid():
            try:
                # Add timestamp to settings data
                settings_data = serializer.validated_data
                settings_data['last_updated'] = datetime.now().isoformat()
                
                # Update or insert settings
                result = user_settings.replace_one({}, settings_data, upsert=True)
                logger.info(f"Settings updated successfully")
                
                return Response(settings_data, status=status.HTTP_200_OK)
            except Exception as e:
                logger.error(f"Error updating settings: {str(e)}")
                return Response(
                    {
                        'error': 'An error occurred while updating settings.',
                        'details': str(e),
                        'message': 'This could be due to a database connection issue. Please check your database connection and try again.'
                    }, 
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class WeatherView(APIView):
    """
    API view for fetching weather data.
    """
    def get(self, request):
        """
        Get weather forecast for a location.
        """
        location = request.query_params.get('location', '')
        
        if not location:
            return Response({'message': 'Location parameter is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Get weather forecast from OpenWeatherMap API
            weather_data = get_weather_forecast(location)
            return Response(weather_data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error fetching weather data: {str(e)}")
            return Response(
                {
                    'error': 'An error occurred while fetching weather data.',
                    'details': str(e),
            
                    'message': 'This could be due to an issue with the OpenWeatherMap API or an invalid location. The application will use default rainfall values as a fallback.'
                }, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
