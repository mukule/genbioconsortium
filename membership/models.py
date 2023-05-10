from django.db import models
from django.contrib.auth import get_user_model
from django_countries.fields import CountryField

CustomUser = get_user_model()

class MembershipCategory(models.Model):
    title = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return self.title

class MembershipRegistration(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    membership_category = models.ForeignKey(MembershipCategory, on_delete=models.CASCADE, null=True)
    membership = models.CharField(max_length=100)
    institution = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    country = CountryField()
    occupation = models.CharField(max_length=100)
    terms_checkbox = models.BooleanField(default=False)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField()
    membership_price = models.DecimalField(max_digits=8, decimal_places=2)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.membership} - {self.first_name} {self.last_name}"

class Payment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    membership_registration = models.ForeignKey(MembershipRegistration, on_delete=models.CASCADE)
    transaction_id = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    full_name = models.CharField(max_length=60)
    membership_type = models.CharField(max_length=100)
    payment_id = models.CharField(max_length=100)
    email = models.EmailField()
    payment_status = models.CharField(max_length=30)
    gross_pay = models.DecimalField(max_digits=8, decimal_places=2)
    paypal_fee = models.DecimalField(max_digits=8, decimal_places=2)
    net_pay = models.DecimalField(max_digits=8, decimal_places=2)
    payer_id = models.CharField(max_length=100)

    def __str__(self):
        return f"Payment for {self.membership_registration} - Transaction ID: {self.transaction_id}"
