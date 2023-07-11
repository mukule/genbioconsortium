from django.urls import path
from . import views

from . views import membershipCategory, CongressCategory



app_name = 'membership'
urlpatterns = [
    path('member_cat/', membershipCategory.as_view(), name='precongress_cat'),
     path('member_cat/', CongressCategory.as_view(), name='congress_cat'),
    path('<int:category_id>/', views.membership_registration, name='membership_registration'),
    path('payment_method/', views.payment_method, name='payment_method'),
    path('congress/members/', views.congress_members, name='congress_members'),

    
]