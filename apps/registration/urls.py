from django.urls import path

"""
This module will define urls for Registration app
"""

from .views import (
    UserRegistrationView,
    HomeView,
)
from django.contrib.auth import views as auth_views

app_name = "registration"
urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("register/", UserRegistrationView.as_view(), name="user-registration"),
    path("login/", auth_views.LoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
]
