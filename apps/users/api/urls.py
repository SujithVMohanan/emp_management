from django.urls import path


from apps.users.api.views import (
    GetUsersApiView,
    LoginAPIView,
    LogoutAPIView,
    RegisterUserApiView,
)


urlpatterns = [
    path('login/', LoginAPIView().as_view(), name='login'),
    path('logout/', LogoutAPIView().as_view(), name='logout'),
    path('register/', RegisterUserApiView().as_view(), name='register'),

    path('list-users/', GetUsersApiView().as_view(), name='list_users'),
]