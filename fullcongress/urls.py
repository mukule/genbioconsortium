from django.urls import path
from . import views

from . views import *



app_name = 'fullcongress'
urlpatterns = [
    path('fullcongress_cat/', fullcongressCategory.as_view(), name='fullcongress_cat'),
    path('<int:category_id>/', views.membership_registration, name='membership_registration'),
    path('members/', fullcongress_members, name='fullcongress_members'),
    # path('payment_method/', views.payment_method, name='payment_method'),
    
]