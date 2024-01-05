from django.db import models

from django.db import models

class WeatherData(models.Model):
    email = models.EmailField()
    location = models.CharField(max_length=255)
    temperature = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

