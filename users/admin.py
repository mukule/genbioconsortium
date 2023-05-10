from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    # Specify the fields to display in the change list
    list_display = ['username', 'email', 'first_name', 'last_name']

    # Specify the fields to use in the search box
    search_fields = ['username', 'email']

    # Customize the fieldsets to display in the edit page
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    # Customize the ordering of fields in the edit page
    # ordering = ['-date_joined']  # Example: Order by date joined descending

admin.site.register(CustomUser, CustomUserAdmin)

