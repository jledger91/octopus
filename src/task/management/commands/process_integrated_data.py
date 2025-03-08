import json

from django.core.management.base import BaseCommand

from src.task.models import (
    Connector,
    Coordinates,
    Country,
    Evse,
    Location,
    Operator,
)


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            "--filepath",
            type=str,
            required=True,
            help="The path of the data file to process.",
        )

    def handle(self, *args, **options):
        filepath = options.get("filepath")

        print(f"Loading data from {filepath}...")

        # TODO: Add some error handling if the file can't be found/opened.
        with open(filepath, "r") as file:
            data = json.load(file)

        # TODO: Ideally, we'd bulk create these, but it we'd need to point
        #  locations to existing related models before saving them. Might get
        #  ugly.
        #  -
        #  Also, there's very little exception handling at the moment, which
        #  isn't great, but I can test manually to iron out any kinks, and
        #  free up time for later parts of the assignment.
        for i, location_data in enumerate(data, 1):
            print(f"Processing location {i}...")

            coordinates, _ = Coordinates.objects.get_or_create(
                lat=location_data["coordinates"]["latitude"],
                lon=location_data["coordinates"]["longitude"],
            )
            country, _ = Country.objects.get_or_create(
                reference=location_data["country"]
            )
            operator = (
                Operator.objects.get_or_create(
                    reference=operator_data["name"]
                )[0]
                if (operator_data := location_data["operator"])
                else None
            )
            location, _ = Location.objects.get_or_create(
                reference=location_data["id"],
                defaults={
                    "country": country,
                    "operator": operator,
                    "coordinates": coordinates,
                    "postal_code": location_data["postal_code"],
                },
            )
            for ii, evs_data in enumerate(location_data["evses"], 1):
                print(f"\tProcessing EVSE {ii}...")

                evse, _ = Evse.objects.get_or_create(
                    location=location,
                    physical_identifier=evs_data["physical_reference"],
                    defaults={
                        "status": evs_data["status"],
                    },
                )
                for iii, connector_data in enumerate(
                    evs_data["connectors"], 1
                ):
                    print(f"\t\tProcessing connector {iii}...")

                    Connector.objects.get_or_create(
                        evse=evse,
                        power=connector_data.get("max_electric_power"),
                        standard=connector_data["standard"],
                    )

        print("Done.")
