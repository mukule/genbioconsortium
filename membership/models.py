from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class MembershipCategory(models.Model):
    title = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return self.title
    
class MembershipRegistration(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    membership_category = models.ForeignKey(MembershipCategory, on_delete=models.CASCADE, null=True)
    membership = models.CharField(max_length=100)
    institution = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    occupation = models.CharField(max_length=100)
    terms_checkbox = models.BooleanField(default=False)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField()
    membership_price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"{self.user.username}'s Membership Registration"
