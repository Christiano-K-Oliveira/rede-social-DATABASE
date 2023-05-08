from django.urls import path
from . import views


urlpatterns = [
    path("followers/", views.FollowersView.as_view()),
    path("follower/<follower_key>/<following_key>/", views.FollowerView.as_view()),
    path("<follower_type>/<follower_key>/", views.FollowerUniqueView.as_view()),
]
