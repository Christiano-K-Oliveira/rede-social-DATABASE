from django.urls import path
from . import views


urlpatterns = [
    path("publication/", views.PublicationView.as_view()),
    path("publication/<publication_key>/", views.PublicationUniqueView.as_view()),
    path("publications_public/", views.PublicationsFreeView.as_view()),
    path("publications/", views.PublicationsPrivateView.as_view()),
    path("timeline/", views.TimelineView.as_view())
]
