from decimal import Decimal
from django.test import TestCase, Client
from django.urls import reverse
from core.models import Vehicle


class VehicleModelTest(TestCase):
    def setUp(self):
        self.vehicle = Vehicle.objects.create(
            name="Caminhão Teste", max_capacity=10000, cost_per_km=Decimal("5.00")
        )

    def test_vehicle_str(self):
        """Testa a representação em string do modelo Vehicle."""
        self.assertEqual(str(self.vehicle), "Caminhão Teste")


class VehicleListViewTest(TestCase):
    def setUp(self):
        self.vehicle1 = Vehicle.objects.create(
            name="Caminhão A", max_capacity=10000, cost_per_km=Decimal("5.00")
        )
        self.vehicle2 = Vehicle.objects.create(
            name="Caminhão B", max_capacity=20000, cost_per_km=Decimal("8.00")
        )
        self.client = Client()

    def test_vehicle_list_view(self):
        """
        Testa a view que lista os veículos, verificando se os nomes dos veículos são exibidos.
        """
        response = self.client.get(reverse("vehicle_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.vehicle1.name)
        self.assertContains(response, self.vehicle2.name)
