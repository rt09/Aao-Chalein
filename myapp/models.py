from time import time
from unittest.util import _MAX_LENGTH
from django.db import models
from django.db import connections
from django.db.models import Model
# from django.conf.locale.es import formats as es_formats
# from django import forms
# from django.forms import ModelForm
from django.utils.timezone import datetime

# Create your models here.


class journeyDetails(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    dayid = models.CharField(max_length=100)
    emailid = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    hall = models.CharField(max_length=100)
    date = models.DateField(max_length=100)
    time = models.TimeField(max_length=100)
    comtime = models.DateTimeField(max_length=100)
    Blocation = models.CharField(max_length=100)
    Dlocation = models.CharField(max_length=100)
    cityfrom = models.CharField(max_length=100)
    cityto = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    comments = models.CharField(
        max_length=100, null=True, default=datetime.today)

    def __str__(self):
        return self.name

    # class Meta:
    #     db_table = 'details'
    #     managed = False


class Loggedin(models.Model):
    id = models.IntegerField(primary_key=True, auto_created=True)
    loggedin = models.CharField(max_length=100)
    time = models.TimeField(max_length=100)
    date = models.DateField(max_length=100)

    # class Meta:
    #     db_table = 'login'
    #     managed = False

    def __str__(self):
        return self.loggedin


class contactinfo(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    subject = models.CharField(max_length=100)
    message = models.CharField(max_length=200)

    # class Meta:
    #     db_table = 'wantstocontact'
    #     managed = False
    def __str__(self):
        return self.name
