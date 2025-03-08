from unittest import skip

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

    def test_location_list_view__country_filter(self):
        self.client.force_login(self.user)

        new_location = LocationFactory()
        new_location_country_reference = new_location.country.reference

        response = self.client.get(
            self.url + f"?country={new_location_country_reference}"
        )
        assert response.status_code == 200

        data = response.json()
        assert len(data) == 1

        location = data[0]
        assert location["country_reference"] == new_location_country_reference

    def test_location_list_view__operator_filter(self):
        self.client.force_login(self.user)

        new_location = LocationFactory()
        new_location_operator_reference = new_location.operator.reference

        response = self.client.get(
            self.url + f"?operator={new_location_operator_reference}"
        )
        assert response.status_code == 200

        data = response.json()
        assert len(data) == 1

        location = data[0]
        assert (
            location["operator_reference"] == new_location_operator_reference
        )

    def test_location_list_view__ordering_filter__created_at_desc(self):
        self.client.force_login(self.user)

        new_location = LocationFactory()

        response = self.client.get(self.url + "?ordering=created_at_desc")
        assert response.status_code == 200

        data = response.json()
        assert data[0]["operator_reference"] == new_location.operator.reference
        assert (
            data[1]["operator_reference"] == self.location.operator.reference
        )

    def test_location_list_view__ordering_filter__updated_at_desc(self):
        self.client.force_login(self.user)

        new_location = LocationFactory()
        self.location.save()

        response = self.client.get(self.url + "?ordering=updated_at_desc")
        assert response.status_code == 200

        data = response.json()
        assert (
            data[0]["operator_reference"] == self.location.operator.reference
        )
        assert data[1]["operator_reference"] == new_location.operator.reference

    @skip("Skipping while this functionality is incomplete.")
    def test_location_list_view__order_by_coordinates(self):
        self.client.force_login(self.user)

        new_location = LocationFactory()
        lon = new_location.coordinates.lon
        lat = new_location.coordinates.lon

        response = self.client.get(
            self.url + f"?order_by_coordinates={lon},{lat}"
        )
        assert response.status_code == 200

        data = response.json()
        assert data[0]["operator_reference"] == new_location.operator.reference
        assert (
            data[1]["operator_reference"] == self.location.operator.reference
        )


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
