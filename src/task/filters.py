import django_filters as filters
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point

from src.task.models import Location


class CoordinatesOrderingFilter(filters.Filter):
    def filter(self, qs, value):
        """
        Allows you to order by latitude and longitude.

        :param qs: The queryset.
        :param value: The coordinates, in the format "{lon},{lat}".
        """

        if not value:
            return qs

        # TODO: Should add error handling, but I'm running out of time, so
        #  I'll assume the value is in the expected format.
        latitude, longitude = value.split(",")
        latitude = float(latitude)
        longitude = float(longitude)

        # TODO: This hasn't been tested, as the migration for
        #  Location.coordinates to a PointField isn't working.
        #  (See: __0004_coordinates_as_point_field.py)
        return qs.annotate(
            distance=Distance(
                "coordinates", Point(longitude, latitude, srid=123)
            )
        ).order_by("distance")


class LocationFilterSet(filters.FilterSet):
    country = filters.CharFilter(field_name="country__reference")
    operator = filters.CharFilter(field_name="operator__reference")
    ordering = filters.OrderingFilter(
        fields=[
            ("-created_at", "created_at_desc"),
            ("-updated_at", "updated_at_desc"),
        ]
    )
    order_by_coordinates = CoordinatesOrderingFilter()

    class Meta:
        model = Location
        fields = [
            "country",
            "operator",
            "ordering",
            "order_by_coordinates",
        ]
