from django.db import models
import json

class UserInput(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    data = models.JSONField()

    def __str__(self):
        return f"Input at {self.timestamp}"

class CalculationResult(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    input_data = models.ForeignKey(UserInput, on_delete=models.CASCADE, related_name='results')
    data = models.JSONField()

    def __str__(self):
        return f"Result at {self.timestamp}"

class HistoricalData(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    data = models.JSONField()

    def __str__(self):
        return f"Historical data at {self.timestamp}"

class UserSettings(models.Model):
    data = models.JSONField()
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Settings last updated at {self.last_updated}"
