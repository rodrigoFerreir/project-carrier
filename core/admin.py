from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Vehicle, TransportCalculation
from .resources import VehicleResource

# Register your models here.
# admin.site.register(Vehicle)
admin.site.register(TransportCalculation)


@admin.register(Vehicle)
class VehicleAdmin(ImportExportModelAdmin):
    resource_class = VehicleResource
    list_display = ("name", "max_capacity", "cost_per_km")
