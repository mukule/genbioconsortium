from django.urls import path
from . import views

from . views import *



app_name = 'precongress'
urlpatterns = [
    path('precongress_cat/', precongressCategory.as_view(), name='precongress_cat'),
    path('<int:category_id>/', views.membership_registration, name='membership_registration'),
    # path('payment_method/', views.payment_method, name='payment_method'),
    
]