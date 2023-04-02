from django.urls import path
from .views import payment_canceled, create_paypal_order, paypal_webhook


from . import views


app_name = 'payment'
urlpatterns = [
    path('payment_done/', views.payment_done, name='payment_done'),
    path('canceled/', payment_canceled, name='payment_canceled'),
    path('create_paypal_order', create_paypal_order, name='create_paypal_order'),
    path('paypal_webhook', views.paypal_webhook, name='paypal_webhook'),
    
]