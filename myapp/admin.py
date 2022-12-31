from django.contrib import admin
from .models import journeyDetails, Loggedin, contactinfo


# Register your models here.
admin.site.register(journeyDetails)
admin.site.register(Loggedin)
admin.site.register(contactinfo)
