from django.db import models

# Create your models here.
class Cluster(models.Model):
    latitude = models.FloatField()
    longtitude = models.FloatField()
    timestamp = models.FloatField()
    cluster = models.TextField()
    source = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
