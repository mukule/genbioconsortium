from django.urls import path

from . import views
urlpatterns = [
    path("payment", views.index, name="index"),
    # path('payment/callback/', views.payment_callback, name='payment_callback'),
    path('payment_complete/', views.payment_complete, name='payment_complete'),
    path('payment_fail', views.payment_fail, name='payment_fail'),
    path('payment_success', views.payment_success, name='payment_success'),
    path('payment_complete_error', views.payment_complete_error, name='payment_complete_error'),
    
    
]