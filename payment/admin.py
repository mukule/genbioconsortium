from django.contrib import admin
from payment.models import Event, Ticket, Payment

# Register your models here.
admin.site.register(Event)
admin.site.register(Ticket)
admin.site.register(Payment)