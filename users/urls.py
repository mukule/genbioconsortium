from django.urls import path
from .import views

from django.contrib.auth import views as auth_view

urlpatterns = [
    # path('', views.home, name='home'),
    path("register", views.register, name="register"),
    path('', views.customized_login, name='login'),
    path('logout', views.customized_logout, name='logout'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('profile/<username>', views.profile, name='profile'),
    path("password_change", views.password_change, name="password_change"),
    path("password_reset", views.password_reset_request, name="password_reset"),
    path('reset/<uidb64>/<token>', views.passwordResetConfirm, name='password_reset_confirm'),
]