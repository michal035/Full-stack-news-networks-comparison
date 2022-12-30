from django.db import models


class um(models.Model):
    headline = models.CharField(max_length=255)
    adate = models.DateField()


    def __str__(self):
        return self.headline

class tvn(models.Model):
    id =  models.AutoField(primary_key=True)
    headline = models.CharField(max_length=255)
    date = models.DateField()
    hour = models.CharField(max_length=5, blank=True)
    link = models.CharField(max_length=255, blank=True)


    def __str__(self):
        return self.headline


class tvp(models.Model):
    id =  models.AutoField(primary_key=True)
    headline = models.CharField(max_length=255)
    date = models.DateField()
    hour = models.CharField(max_length=5, blank=True)
    link = models.CharField(max_length=255, blank=True)


    def __str__(self):
        return self.headline
