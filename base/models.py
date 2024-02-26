from django.db import models

# Create your models here.
class Floor(models.Model):
    name = models.CharField(max_length=50)

class Camera(models.Model):
    name = models.CharField(max_length=50)
    url = models.URLField()

