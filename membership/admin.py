from django.contrib import admin
from .models import MembershipCategory,MembershipRegistration,Payment

# Register your models here.

admin.site.register(MembershipCategory)
admin.site.register(MembershipRegistration)
admin.site.register(Payment)

