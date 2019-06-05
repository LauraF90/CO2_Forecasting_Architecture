from django.db import models

# The forecasts model.
class Forecasts(models.Model):
    hour = models.IntegerField()

    co2 = models.FloatField()    


    def __str__(self):
        return "{} - {}".format(self.hour, self.co2)