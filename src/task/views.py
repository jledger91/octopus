from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated

from src.task.models import Location
from src.task.serializers import (
    LocationDetailSerializer,
    LocationListSerializer,
)


class LocationListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LocationListSerializer
    queryset = Location.objects.all()


class LocationDetailView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LocationDetailSerializer
    queryset = Location.objects.all()
    lookup_field = "reference"
