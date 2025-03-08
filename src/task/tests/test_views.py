import pytest
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from src.task.tests.factories import (
    ConnectorFactory,
    EvseFactory,
    LocationFactory,
)


@pytest.mark.django_db
class LocationListViewTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

        cls.location = LocationFactory()
        for _ in range(2):
            EvseFactory(location=cls.location)

        cls.url = reverse("locations")
        cls.user = User.objects.create_user("test_user")

    def test_location_list_view__ok(self):
        self.client.force_login(self.user)

        response = self.client.get(self.url)
        assert response.status_code == 200

        data = response.json()
        assert len(data) == 1

        location = data[0]
        assert location["coordinates"]["lat"] == self.location.coordinates.lat
        assert location["coordinates"]["lon"] == self.location.coordinates.lon
        assert (
            location["operator_reference"] == self.location.operator.reference
        )
        assert location["country_reference"] == self.location.country.reference
        assert location["postal_code"] == self.location.postal_code
        assert location["number_of_evses"] == self.location.evses.count() == 2

    def test_location_list_view__403(self):
        response = self.client.get(self.url)
        assert response.status_code == 403


@pytest.mark.django_db
class LocationDetailViewTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

        cls.location = LocationFactory()
        cls.evse = EvseFactory(location=cls.location)
        cls.connector = ConnectorFactory(evse=cls.evse)

        cls.url = reverse(
            "location", kwargs={"reference": cls.location.reference}
        )
        cls.user = User.objects.create_user("test_user")

    def test_location_detail_view__ok(self):
        self.client.force_login(self.user)

        response = self.client.get(self.url)
        assert response.status_code == 200

        location = response.json()
        assert location["coordinates"]["lat"] == self.location.coordinates.lat
        assert location["coordinates"]["lon"] == self.location.coordinates.lon
        assert (
            location["operator_reference"] == self.location.operator.reference
        )
        assert location["country_reference"] == self.location.country.reference
        assert location["postal_code"] == self.location.postal_code
        assert len(location["evses"]) == self.location.evses.count() == 1

        evse = location["evses"][0]
        assert evse["physical_identifier"] == self.evse.physical_identifier
        assert evse["status"] == self.evse.status
        assert len(evse["connectors"]) == self.evse.connectors.count() == 1

        connector = evse["connectors"][0]
        assert connector["power"] == self.connector.power
        assert connector["standard"] == self.connector.standard

    def test_location_detail_view__403(self):
        response = self.client.get(self.url)
        assert response.status_code == 403
