from django.urls import path

from src.task.views import LocationDetailView, LocationListView

urlpatterns = [
    path(
        "location/<str:reference>",
        LocationDetailView.as_view(),
        name="location",
    ),
    path("locations", LocationListView.as_view(), name="locations"),
]
