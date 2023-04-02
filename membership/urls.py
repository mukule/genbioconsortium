from django.urls import path
from . import views

from . views import membershipCategory



app_name = 'membership'
urlpatterns = [
    path('member_cat/', membershipCategory.as_view(), name='member_cat'),
    path('<int:category_id>/', views.membership_registration, name='membership_registration'),
    path('payment_method/', views.payment_method, name='payment_method'),
    
]