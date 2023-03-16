from django.urls import path
from .import views

from django.contrib.auth import views as auth_view

urlpatterns = [
    path('', views.register, name='register'),
    path('login/', auth_view.LoginView.as_view(template_name = 'users/login.html'), name='login'),
    path('logout/', auth_view.LogoutView.as_view(template_name = 'users/logout.html'), name='logout'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('profile/<username>', views.profile, name='profile'),
    path("password_change", views.password_change, name="password_change"),
]