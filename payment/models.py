from django.db import models
from django.contrib.auth.models import User
from django.db import models
from django.conf import settings
from django_countries.fields import CountryField

from django.db import models

from django.db import models

class Event(models.Model):
    event_name = models.CharField(max_length=255)
    description = models.TextField(default='description not provided')
    event_date = models.DateField()
    venue = models.CharField(max_length=255)
    fee = models.DecimalField(max_digits=10, decimal_places=2, default=1)
    
    def __str__(self):
        return self.event_name

class Ticket(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    num_tickets = models.PositiveIntegerField()
    ticket_number = models.CharField(max_length=20, unique=True, blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    paid = models.BooleanField(default=False)
    payer_email = models.EmailField(blank=True)
    country_code = models.CharField(max_length=2, blank=True)
    time_paid = models.DateTimeField(null=True)
    currency = models.CharField(max_length=3, blank=True)

    def save(self, *args, **kwargs):
        if not self.ticket_number:
            num_tickets_sold = Ticket.objects.filter(event=self.event).count()
            self.ticket_number = f'T{self.event.id:06d}-{num_tickets_sold+1:06d}'
        
        super().save(*args, **kwargs)

    def __str__(self):
        return self.ticket_number

    class Meta:
        ordering = ['ticket_number']


class Receipt(models.Model):
    ticket = models.OneToOneField('Ticket', on_delete=models.CASCADE)
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=50)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Receipt for ticket {self.ticket.ticket_number}"

    
class Payment(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("COMPLETED", "Completed"),
        ("CANCELLED", "Cancelled"),
        ("REFUNDED", "Refunded"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    amount_paid = models.DecimalField(max_digits=6, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    paypal_transaction_id = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(
        max_length=10, choices=PAYMENT_STATUS_CHOICES, default="PENDING"
    )

    def __str__(self):
        return f"{self.ticket} - {self.amount_paid}"
