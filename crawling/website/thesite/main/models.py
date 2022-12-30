from django.db import models


class um(models.Model):
    headline = models.CharField(max_length=255)
    adate = models.DateField()

    def __str__(self):
        return self.headline