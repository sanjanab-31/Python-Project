"""
URL patterns for the rainwater harvester API.
"""
from django.urls import path
from .views import (
    InputsView,
    ResultsView,
    SaveResultsView,
    WeatherView,
    HistoricalDataView,
    SettingsView
)

urlpatterns = [
    path('inputs/', InputsView.as_view(), name='inputs'),
    path('results/', ResultsView.as_view(), name='results'),
    path('save-results/', SaveResultsView.as_view(), name='save-results'),
    path('weather/', WeatherView.as_view(), name='weather'),
    path('historical-data/', HistoricalDataView.as_view(), name='historical-data'),
    path('historical-data/<str:result_id>/', HistoricalDataView.as_view(), name='delete-historical-data'),
    path('settings/', SettingsView.as_view(), name='settings'),
]
