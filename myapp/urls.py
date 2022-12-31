from atexit import register
from typing import Counter
from unicodedata import name
from django.urls import path
from . import views


urlpatterns = [
    path('save', views.save, name='save'),
    path('register', views.register, name='register'),
    path('Login', views.Login, name='Login'),
    path('search', views.search, name='search'),
    path('Result', views.Result, name='Result'),
    path('', views.home, name='home'),
    path('trips', views.trips, name='trips'),
    path('dash', views.dash, name='dash'),
    path("otp", views.otp, name="otp"),
    # path("dates", views.dates, name="dates"),
    path("contact", views.contact, name="contact"),
    # path("delogin", views.delogin, name="delogin"),
    # path("", views.home1, name="home1"),
    # path("send_otp", views.send_otp, name="send otp"),
]
