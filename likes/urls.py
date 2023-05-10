from django.urls import path
from . import views


urlpatterns = [
    path("like/", views.LikeView.as_view()),
    path("like/<publication_key>/", views.LikeUniqueView.as_view())
]
