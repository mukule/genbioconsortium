from django.contrib import admin

# Register your models here.

from .models import Transaction, Amount

admin.site.register(Transaction)
admin.site.register(Amount)
