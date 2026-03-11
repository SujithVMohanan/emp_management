

from django.urls import path
from apps.users.views import (
    HomeView,
    LoginView,
    LogoutView,
    ProfileView,
    RegisterView,
    ChangePasswordView,
)
app_name = "users"
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('login/', LoginView.as_view(), name='auth_login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
    path('profile/', ProfileView.as_view(), name='profile'),
    
]