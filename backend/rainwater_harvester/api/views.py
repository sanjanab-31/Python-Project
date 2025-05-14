"""
Views for the rainwater harvester API.
"""
from datetime import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import json
import logging
from .serializers import InputSerializer, SettingsSerializer, ResultIdSerializer
from .calculation_service import process_inputs
from .weather_service import get_weather_forecast
from .models import UserInput, CalculationResult, HistoricalData, UserSettings

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
                
                # Save inputs to database
                user_input = UserInput.objects.create(data=input_data)
                input_id = user_input.id
                logger.info(f"Input data saved to database with ID: {input_id}")
                
                # Add input ID to input data
                input_data['_id'] = input_id
                
                # Process inputs and get results
                results = process_inputs(input_data)
                
                # Add input ID to results
                results['input_id'] = input_id
                
                # Save results
                result = CalculationResult.objects.create(
                    input_data=user_input,
                    data=results
                )
                logger.info("Results saved to database")
                
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
                result = CalculationResult.objects.filter(input_data__id=user_input_id).last()
                if result:
                    return Response(result.data, status=status.HTTP_200_OK)
                else:
                    return Response({'message': 'No results found for the given input ID'}, status=status.HTTP_404_NOT_FOUND)
            else:
                logger.info("Fetching latest results")
                result = CalculationResult.objects.last()
                if result:
                    return Response(result.data, status=status.HTTP_200_OK)
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
            # Extract key data for historical analysis
            data = request.data
            
            historical_data = {
                'timestamp': datetime.now().isoformat(),
                'location': data.get('inputs', {}).get('location', ''),
                'roofArea': data.get('inputs', {}).get('roofArea', 0),
                'tankCapacity': data.get('inputs', {}).get('tankCapacity', 0),
                'inflow': data.get('inflow', {}).get('dailyInflow', 0),
                'outflow': data.get('inputs', {}).get('outflow', 0),
                'rainfall': data.get('weatherData', {}).get('averageRainfall', 0),
                'currentLevel': data.get('inputs', {}).get('tankCapacity', 0) * 0.5,  # Assume 50% for now
                'waterUsage': data.get('waterUsage', {}),
                'isLeaking': data.get('leakDetection', {}).get('isLeaking', False)
            }
            
            # Save to historical data collection
            HistoricalData.objects.create(data=historical_data)
            
            return Response({'message': 'Results saved successfully'}, status=status.HTTP_201_CREATED)
        
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
    API view for retrieving historical data.
    """
    def get(self, request):
        """
        Get historical data for analysis.
        """
        try:
            # Get historical data from database
            historical_data = list(HistoricalData.objects.order_by('-timestamp').values('data'))
            return Response([item['data'] for item in historical_data], status=status.HTTP_200_OK)
        
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
            settings = UserSettings.objects.first()
            if settings:
                return Response(settings.data, status=status.HTTP_200_OK)
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
                settings_data['timestamp'] = datetime.now().isoformat()
                
                # Save settings to database
                settings, created = UserSettings.objects.get_or_create(id=1)
                settings.data = settings_data
                settings.save()
                
                return Response({'message': 'Settings updated successfully'}, status=status.HTTP_200_OK)
            
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

class DeleteSavedResultsView(APIView):
    """
    API view for deleting saved results.
    """
    def delete(self, request):
        """
        Delete a saved result by ID.
        """
        serializer = ResultIdSerializer(data=request.query_params)
        
        if serializer.is_valid():
            try:
                result_id = serializer.validated_data.get('id')
                
                if not result_id:
                    return Response(
                        {'message': 'Result ID is required'}, 
                        status=status.HTTP_400_BAD_REQUEST
                    )
                
                try:
                    # Delete result from database
                    result = CalculationResult.objects.filter(id=result_id).first()
                    if result:
                        result.delete()
                        return Response({'message': 'Result deleted successfully'}, status=status.HTTP_200_OK)
                    else:
                        return Response({'message': 'Result not found'}, status=status.HTTP_404_NOT_FOUND)
                except ValueError:
                    return Response(
                        {'message': 'Invalid result ID format'}, 
                        status=status.HTTP_400_BAD_REQUEST
                    )
            
            except Exception as e:
                logger.error(f"Error deleting result: {str(e)}")
                return Response(
                    {
                        'error': 'An error occurred while deleting the result.',
                        'details': str(e),
                        'message': 'This could be due to a database connection issue or an invalid result ID.'
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
