from time import time
from unittest.util import _MAX_LENGTH
from django.db import models
from django.db import connections
from django.db.models import Model
# from django.conf.locale.es import formats as es_formats
# from django import forms
# from django.forms import ModelForm

# Create your models here.


class journeyDetails(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    hall = models.CharField(max_length=100)
    date = models.DateField(max_length=100)
    time = models.TimeField(max_length=100)
    Blocation = models.CharField(max_length=100)
    Dlocation = models.CharField(max_length=100)
    phone=models.CharField(max_length=100)

    class Meta:
        db_table = 'details'
        managed = False

    # def __str__(self):
    #     return self.name
