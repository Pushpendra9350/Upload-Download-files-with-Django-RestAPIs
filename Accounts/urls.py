from django.urls import path
from Accounts import views

# All url patterns for Accounts App
urlpatterns = [
    path('register/', views.RegisterUserAPI.as_view(), name="register"), # New user registration
    path('login/', views.UserLoginAPI.as_view(), name="login"), # Login existing user
]