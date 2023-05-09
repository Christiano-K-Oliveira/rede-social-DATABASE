from django.urls import path
from . import views


urlpatterns = [
    path("friendships/", views.FriendshipView.as_view()),
]
