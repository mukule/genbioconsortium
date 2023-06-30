from django.db import models
from django.contrib.auth import get_user_model
from django_countries.fields import CountryField

CustomUser = get_user_model()

# Create your models here.
class FullcongressCategory(models.Model):
    title = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return self.title

class fullcongressRegistration(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    membership_category = models.ForeignKey(FullcongressCategory, on_delete=models.CASCADE, null=True)
    membership = models.CharField(max_length=100)
    institution = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    country = CountryField()
    occupation = models.CharField(max_length=100)
    terms_checkbox = models.BooleanField(default=False)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField()
    fullcongress_price = models.DecimalField(max_digits=8, decimal_places=2)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.precongress} - {self.first_name} {self.last_name}"
