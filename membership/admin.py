from django.contrib import admin
from .models import RegistrationType, MembershipCategory, MembershipRegistration, Payment

@admin.register(RegistrationType)
class RegistrationTypeAdmin(admin.ModelAdmin):
    pass

@admin.register(MembershipCategory)
class MembershipCategoryAdmin(admin.ModelAdmin):
    pass

@admin.register(MembershipRegistration)
class MembershipRegistrationAdmin(admin.ModelAdmin):
    list_display = ['user', 'registration_type', 'membership_category', 'paid']
    list_filter = ['registration_type', 'membership_category', 'paid']
    search_fields = ['user__username', 'first_name', 'last_name', 'email']

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['user', 'membership_registration', 'transaction_id', 'payment_status']
    list_filter = ['payment_status']
    search_fields = ['user__username', 'membership_registration__first_name', 'membership_registration__last_name', 'transaction_id', 'email']
