"""
Serializers for the rainwater harvester API.
"""
from rest_framework import serializers

class InputSerializer(serializers.Serializer):
    """
    Serializer for user inputs.
    """
    _id = serializers.CharField(read_only=True)
    roofArea = serializers.FloatField(required=True)
    outflow = serializers.FloatField(required=True)
    location = serializers.CharField(required=True)
    tankCapacity = serializers.FloatField(required=True)
    waterCostPerLiter = serializers.FloatField(required=False, default=0.002)
    setupCost = serializers.FloatField(required=False, default=5000)
    maintenanceCost = serializers.FloatField(required=False, default=500)

class SettingsSerializer(serializers.Serializer):
    """
    Serializer for user settings.
    """
    data = serializers.JSONField()
    alertForCleaning = serializers.BooleanField(required=False, default=True)

class ResultIdSerializer(serializers.Serializer):
    """
    Serializer for result ID.
    """
    id = serializers.IntegerField(required=True)

class ResultIdSerializer(serializers.Serializer):
    """
    Serializer for result ID.
    """
    id = serializers.CharField(required=True)
