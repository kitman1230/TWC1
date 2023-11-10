from django.db import models


# Create your models here.
class ENERGY(models.Model):
    energyYear = models.PositiveIntegerField()
    energyType = models.CharField(max_length=100)
    energyUsed = models.FloatField()

    class Meta:
        ordering = ("energyYear", "energyType")
