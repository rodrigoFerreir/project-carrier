from django.urls import path
from .views import (
    VehicleListView,
    CostCalculationView,
    CalculationListView,
    ImportVehiclesView,
    DocumentUploadView,
    DriverValidateView,
    DriverSuccessView,
    DriverListView,
    DriverDetailView,
)

urlpatterns = [
    path("veiculos/", VehicleListView.as_view(), name="vehicle_list"),
    path("calcular-custo/", CostCalculationView.as_view(), name="calculate_cost"),
    path("calculos/", CalculationListView.as_view(), name="calculation_list"),
    path("importar-veiculos/", ImportVehiclesView.as_view(), name="import_vehicles"),
    path('drivers/new/', DocumentUploadView.as_view(), name='driver_upload'),
    path('drivers/validate/', DriverValidateView.as_view(), name='driver_validate'),
    path('drivers/success/', DriverSuccessView.as_view(), name='driver_success'),
    path('drivers/', DriverListView.as_view(), name='driver_list'),
    path('drivers/<int:pk>/', DriverDetailView.as_view(), name='driver_detail'),
]
