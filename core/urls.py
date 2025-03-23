from django.urls import path
from .views import (
    VehicleListView,
    CostCalculationView,
    CalculationListView,
    ImportVehiclesView,
)

urlpatterns = [
    path("", VehicleListView.as_view(), name="vehicle_list"),
    path("veiculos/", VehicleListView.as_view(), name="vehicle_list"),
    path("calcular-custo/", CostCalculationView.as_view(), name="calculate_cost"),
    path("calculos/", CalculationListView.as_view(), name="calculation_list"),
    path("importar-veiculos/", ImportVehiclesView.as_view(), name="import_vehicles"),
]
