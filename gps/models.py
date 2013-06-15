from django.db import models

# Create your models here.
class Track(models.Model):
    latitude=models.FloatField()
    longitude=models.FloatField()
    altitude=models.IntegerField()
    datetime=models.CharField(max_length=25)
    user=models.CharField(max_length=50) 
    waypoint=models.CharField(max_length=50)
    
class Place(models.Model):
    place=models.CharField(max_length=50)
    user=models.CharField(max_length=50)
    latitude=models.FloatField()
    longitude=models.FloatField()

    
    

