from django.contrib import admin

# Register your models here.
from .models import Portfolio,Newestimg

admin.site.register(Portfolio)
admin.site.register(Newestimg)