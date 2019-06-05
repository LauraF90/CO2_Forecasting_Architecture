from rest_framework import generics
from .models import Forecasts
from .serializers import ForecastsSerializer
from .scripts import scripts
# The forecastsview to provid the CO2 emissions forecasts using a GET request
class ListForecastsView(generics.ListAPIView):
    s = scripts()
    
    queryset = s.prediction()
    serializer_class = ForecastsSerializer


