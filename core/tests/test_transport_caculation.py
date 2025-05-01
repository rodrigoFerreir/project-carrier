from decimal import Decimal
from django.test import TestCase
from core.models import Vehicle, TransportCalculation
from core.services import TransportCalculator


class TransportCalculationModelTest(TestCase):
    def setUp(self):
        self.vehicle = Vehicle.objects.create(
            name="Caminhão Teste", max_capacity=10000, cost_per_km=Decimal("5.00")
        )
        self.calculation = TransportCalculation.objects.create(
            vehicle=self.vehicle,
            weight=5000,
            distance=600,
            total_cost=Decimal("3000.00"),
        )

    def test_transport_calculation_str(self):
        """Testa a representação em string do modelo TransportCalculation."""
        expected = f"{self.vehicle.name} - 5000kg - 600km - R$ 3000.00"
        self.assertEqual(str(self.calculation), expected)


class TransportCalculatorServiceTest(TestCase):
    def setUp(self):
        self.vehicle = Vehicle.objects.create(
            name="Caminhão Teste", max_capacity=10000, cost_per_km=Decimal("5.00")
        )
        self.calculator = TransportCalculator()

    def test_calculate_cost_with_vehicle_valid(self):
        """
        Testa o cálculo do custo quando o peso está dentro da capacidade do veículo.
        Para 600 km, com custo 5.00 por km, o custo esperado é 5.00 * 600 = 3000.00.
        """
        cost = self.calculator.calculate_cost_with_vehicle(self.vehicle, 8000, 600)
        expected_cost = self.vehicle.cost_per_km * 600  # 5.00 * 600 = 3000.00
        self.assertEqual(cost, expected_cost)

    def test_calculate_cost_with_vehicle_invalid(self):
        """
        Testa se é levantada uma exceção quando o peso informado excede a capacidade do veículo.
        """
        with self.assertRaises(ValueError):
            self.calculator.calculate_cost_with_vehicle(self.vehicle, 12000, 600)
