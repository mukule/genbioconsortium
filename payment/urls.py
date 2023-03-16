from django.urls import path

from . import views
urlpatterns = [
    path("payment", views. initiate_payment, name="index"),
    # path('payment/callback/', views.payment_callback, name='payment_callback'),
    path('payment_complete/', views.payment_complete, name='payment_complete'),
    path('payment_error', views.payment_error, name='payment_error'),
    # path("checkout/", views.MpesaCheckout.as_view(), name="checkout"),
    # path("callback/", views.MpesaCallBack.as_view(), name="callback"),
    
]