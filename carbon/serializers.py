
from rest_framework import serializers
from .models import Forecasts

# serializing the Forecasts model
class ForecastsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Forecasts 
        fields = ("hour", "co2") 