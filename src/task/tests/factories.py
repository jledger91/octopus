import factory.fuzzy

from src.task.models import (
    Connector,
    Coordinates,
    Country,
    Evse,
    Location,
    Operator,
)


class CoordinatesFactory(factory.django.DjangoModelFactory):
    lat = factory.fuzzy.FuzzyFloat(-90, 90)
    lon = factory.fuzzy.FuzzyFloat(-180, 180)

    class Meta:
        model = Coordinates


class OperatorFactory(factory.django.DjangoModelFactory):
    reference = factory.Faker("uuid4")

    class Meta:
        model = Operator


class CountryFactory(factory.django.DjangoModelFactory):
    reference = factory.Faker("uuid4")

    class Meta:
        model = Country


class LocationFactory(factory.django.DjangoModelFactory):
    reference = factory.Faker("uuid4")
    coordinates = factory.SubFactory(CoordinatesFactory)
    operator = factory.SubFactory(OperatorFactory)
    country = factory.SubFactory(CountryFactory)
    postal_code = factory.Faker("pystr")

    class Meta:
        model = Location


class EvseFactory(factory.django.DjangoModelFactory):
    location = factory.SubFactory(LocationFactory)
    physical_identifier = factory.Faker("uuid4")
    status = factory.Faker("pystr")

    class Meta:
        model = Evse


class ConnectorFactory(factory.django.DjangoModelFactory):
    evse = factory.SubFactory(EvseFactory)
    power = factory.Faker("pyint")
    standard = factory.Faker("pystr")

    class Meta:
        model = Connector
