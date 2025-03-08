from django.contrib import admin

from src.task.models import Country, Location, Operator


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ["reference", "country", "postal_code", "operator"]


@admin.register(Operator)
class OperatorAdmin(admin.ModelAdmin):
    pass


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    pass
