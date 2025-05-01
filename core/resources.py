from import_export import resources
from .models import Vehicle


class VehicleResource(resources.ModelResource):
    class Meta:
        model = Vehicle
        fields = ("id", "name", "max_capacity", "cost_per_km")
