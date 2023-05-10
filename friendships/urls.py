from django.urls import path
from . import views


urlpatterns = [
    path("friendships/", views.FriendshipView.as_view()),
    path("friendship_request/<friendship_key>/", views.FriendshipRequestUniqueView.as_view()),
    path("friendship/<friendship_key>/", views.FriendshipFriendshipUniqueView.as_view()),
    path("friendship/<friendship_request_key>/<friendship_key>/", views.FriendshipRequestKeysView.as_view()),
]
