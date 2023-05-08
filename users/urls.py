from django.urls import path
from . import views
from rest_framework_simplejwt import views as jwt_views


urlpatterns = [
    path("users/", views.UserView.as_view()),
    path("users/<user_key>/", views.UserDetailView.as_view()),
    path("login/", views.LoginView .as_view()),
]
