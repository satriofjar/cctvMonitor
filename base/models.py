from django.db import models

# Create your models here.
class Floor(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Camera(models.Model):
    name = models.CharField(max_length=50)
    url = models.CharField(max_length=255)
    floor = models.ForeignKey(Floor, on_delete=models.CASCADE)

    def __str__(self):
        return self.name