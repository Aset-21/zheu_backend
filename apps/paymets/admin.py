# apps/paymets/admin.py
from django.contrib import admin
from .models import Bank, Payment

admin.site.register(Bank)
admin.site.register(Payment)