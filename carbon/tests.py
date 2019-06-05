from django.test import TestCase

# Create your tests here.
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status
from .models import Forecasts
from .serializers import ForecastsSerializer

# tests for views

# Unit testing for the Forecastsview
class BaseViewTest(APITestCase):
    client = APIClient()

    @staticmethod
    def create_forecast(hour=int, co2=float):
        if hour < 24 and co2 < 2000:
            Forecasts.objects.create(hour=hour, co2=co2)

    def setUp(self):
        # add test data
        self.create_forecast(0,100)
        self.create_forecast(1,70.7)
        self.create_forecast(9,898)
        self.create_forecast(22,889.77)


class GetAllForecastsTest(BaseViewTest):

    def test_get_all_forecasts(self):
        """
        This test ensures that all songs added in the setUp method
        exist when we make a GET request to the songs/ endpoint
        """
        # hit the API endpoint
        response = self.client.get(
            reverse("forecasts-all")
        )
        # fetch the data from db
        expected = Forecasts.objects.all()
        serialized = ForecastsSerializer(expected, many=True)
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
# Create your tests here.
