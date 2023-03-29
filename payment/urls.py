from django.urls import path
from .views import payment_canceled, create_paypal_order, capture_paypal_order
from .views import (
    EventListView, 
    EventDetailView, 
    
)
from . import views



app_name = 'payment'
urlpatterns = [
    path('', EventListView.as_view(), name='index'),
    path('<int:pk>', EventDetailView.as_view(), name='event_detail'),
    path('payment_done/', views.payment_done, name='payment_done'),
    path('canceled/', payment_canceled, name='payment_canceled'),
    path('order/<int:event_id>/', create_paypal_order, name='order'),
    path('complete/<int:event_id>/', capture_paypal_order, name='complete' ),
    
]