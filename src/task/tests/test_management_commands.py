import pytest
from django.core.management import call_command
from django.test import TestCase

from src.task.models import (
    Connector,
    Coordinates,
    Country,
    Evse,
    Location,
    Operator,
)


@pytest.mark.django_db
class ProcessIntegratedDataTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.filepath = "data/integrated.json"

    def test_process_integrated_data__ok(self):
        # TODO: This could probably be doing more, but I mainly want to see
        #  that it runs without error and creates model instances.
        #  -
        #  Ideally, we'd use a simpler file for the data and we could inspect
        #  the instances more thoroughly, but to save time, I've opted for a
        #  simpler test.

        call_command("process_integrated_data", filepath=self.filepath)

        for model in (
            Connector,
            Coordinates,
            Country,
            Evse,
            Location,
            Operator,
        ):
            with self.subTest(model=model.__name__):
                self.assertTrue(model.objects.exists())
