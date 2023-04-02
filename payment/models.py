from django.db import models
from django.contrib.auth.models import User

from django.db import models

class Amount(models.Model):
    amount = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return str(self.amount)


class Transaction(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=1.00)
    phone = models.CharField(max_length=20)
    transaction_id = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s transaction of {self.amount} on {self.timestamp}"