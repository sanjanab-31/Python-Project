from djongo import models
from django.utils import timezone
import json

class UserInput(models.Model):
    _id = models.ObjectIdField()
    timestamp = models.DateTimeField(default=timezone.now)
    data = models.JSONField(default=dict)

    def __str__(self):
        return f"Input at {self.timestamp}"

    class Meta:
        app_label = 'api'
        db_table = 'user_inputs'

class CalculationResult(models.Model):
    _id = models.ObjectIdField()
    timestamp = models.DateTimeField(default=timezone.now)
    input_data = models.EmbeddedField(model_container=UserInput, null=True)
    data = models.JSONField(default=dict)

    def __str__(self):
        return f"Result at {self.timestamp}"

    class Meta:
        app_label = 'api'
        db_table = 'calculation_results'

class HistoricalData(models.Model):
    _id = models.ObjectIdField()
    timestamp = models.DateTimeField(default=timezone.now)
    data = models.JSONField(default=dict)

    def __str__(self):
        return f"Historical data at {self.timestamp}"

    class Meta:
        app_label = 'api'
        db_table = 'historical_data'

class UserSettings(models.Model):
    _id = models.ObjectIdField()
    data = models.JSONField(default=dict)
    last_updated = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Settings last updated at {self.last_updated}"

    class Meta:
        app_label = 'api'
        db_table = 'user_settings'
