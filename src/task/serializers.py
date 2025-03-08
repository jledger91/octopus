from rest_framework import serializers

from src.task.models import Connector, Coordinates, Evse, Location


class ConnectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Connector
        fields = ["power", "standard"]


class EvseSerializer(serializers.ModelSerializer):
    connectors = ConnectorSerializer(many=True, read_only=True)

    class Meta:
        model = Evse
        fields = ["physical_identifier", "status", "connectors"]


class CoordinatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coordinates
        fields = ["lat", "lon"]


class LocationSerializer(serializers.ModelSerializer):
    coordinates = CoordinatesSerializer(read_only=True)
    operator_reference = serializers.CharField(
        source="operator.reference", read_only=True
    )
    country_reference = serializers.CharField(
        source="country.reference", read_only=True
    )

    class Meta:
        model = Location
        fields = [
            "coordinates",
            "operator_reference",
            "country_reference",
            "postal_code",
        ]


class LocationListSerializer(LocationSerializer):
    number_of_evses = serializers.SerializerMethodField()

    def get_number_of_evses(self, obj: Location) -> int:
        return obj.evses.count()

    class Meta(LocationSerializer.Meta):
        fields = LocationSerializer.Meta.fields + ["number_of_evses"]


class LocationDetailSerializer(LocationSerializer):
    evses = EvseSerializer(many=True, read_only=True)

    class Meta(LocationSerializer.Meta):
        fields = LocationSerializer.Meta.fields + ["evses"]
