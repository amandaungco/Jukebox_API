from django.db import models

# Create your models here.
class Track(models.Model):
    title = models.CharField(max_length=100)
    artist = models.CharField(max_length=100)
