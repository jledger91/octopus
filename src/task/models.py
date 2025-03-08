from django.contrib.gis.db import models
from django.db.models import UniqueConstraint

from src.task.base_models import TimeStampedModel


class Coordinates(models.Model):
    lat = models.FloatField()
    lon = models.FloatField()

    class Meta:
        constraints = [
            UniqueConstraint(fields=("lat", "lon"), name="unique_coordinates"),
        ]

    def __str__(self):
        return f"{self.lat}, {self.lon}"


class Operator(models.Model):
    reference = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.reference


class Country(models.Model):
    reference = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = "countries"

    def __str__(self):
        return self.reference


class Location(TimeStampedModel):
    reference = models.CharField(max_length=100, unique=True)
    # FIXME: This isn't currently working.
    #  (see __0004_coordinates_as_point_field.py)
    # coordinates = models.PointField()
    coordinates = models.OneToOneField(Coordinates, on_delete=models.CASCADE)
    operator = models.ForeignKey(
        Operator, related_name="locations", null=True, on_delete=models.CASCADE
    )
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    # TODO: Would this want to be unique?
    #  - What if two countries have the same code for separate locations?
    #  - What if the format was different for two instances of the same code?
    #    We'd have to sanitise.
    #  - If not, would we want to index this?
    postal_code = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.country}, {self.postal_code}"


class Evse(models.Model):
    location = models.ForeignKey(
        Location, related_name="evses", on_delete=models.CASCADE
    )
    physical_identifier = models.CharField(max_length=100, unique=True)
    # TODO: Would preferably use choices for this if I knew all of the
    #  expected statuses.
    status = models.CharField(max_length=100)

    def __str__(self):
        return self.physical_identifier


class Connector(models.Model):
    evse = models.ForeignKey(
        Evse, related_name="connectors", on_delete=models.CASCADE
    )
    # TODO: Made this nullable since it's not present on every connector in
    #  the data, though I'm aware it's specified as int and not `int | None`
    #  on the brief. (This is assuming that `max_electric_power` is the field
    #  we need here.)
    power = models.IntegerField(null=True)
    standard = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.evse}, {self.standard}"
