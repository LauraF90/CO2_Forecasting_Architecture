from django.urls import path
from .views import ListForecastsView


urlpatterns = [
    path('forecasts/', ListForecastsView.as_view(), name="forecasts-all")
]