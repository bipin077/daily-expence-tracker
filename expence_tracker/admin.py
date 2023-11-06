from django.contrib import admin
from .models import ExpenceCategory, Expence, ExpenceMaster

# Register your models here.

admin.site.register(ExpenceCategory)
admin.site.register(Expence)
admin.site.register(ExpenceMaster)
