from decimal import Decimal
from django.test import TestCase, Client
from django.urls import reverse
from core.models import Vehicle, TransportCalculation


class CostCalculationViewTest(TestCase):
    def setUp(self):
        self.vehicle = Vehicle.objects.create(
            name="Caminhão Teste", max_capacity=10000, cost_per_km=Decimal("5.00")
        )
        self.client = Client()

    def test_cost_calculation_view_valid(self):
        """
        Testa a view de cálculo de custo com dados válidos.
        Verifica se o custo é calculado corretamente e se o registro é criado.
        """
        data = {"weight": 8000, "distance": 600, "vehicle": self.vehicle.id}
        response = self.client.post(reverse("calculate_cost"), data)
        self.assertEqual(response.status_code, 200)
        # Verifica se o resultado é exibido na resposta
        self.assertContains(response, "Resultado")
        # Confirma que o cálculo foi registrado no banco de dados
        self.assertEqual(TransportCalculation.objects.count(), 1)
        calculation = TransportCalculation.objects.first()
        self.assertEqual(calculation.vehicle, self.vehicle)
        self.assertEqual(calculation.weight, 8000)
        self.assertEqual(calculation.distance, 600)
        self.assertEqual(calculation.total_cost, Decimal("3000.00"))

    def test_cost_calculation_view_invalid(self):
        """
        Testa a view de cálculo quando o peso informado excede a capacidade do veículo.
        Espera que um erro seja adicionado ao formulário e nenhum registro seja criado.
        """
        data = {
            "weight": 12000,  # Peso que excede a capacidade do veículo (10000 kg)
            "distance": 600,
            "vehicle": self.vehicle.id,
        }
        response = self.client.post(reverse("calculate_cost"), data)
        self.assertEqual(response.status_code, 200)
        # Verifica se a mensagem de erro é apresentada
        self.assertContains(response, "excede a capacidade")
        # Confirma que nenhum cálculo foi registrado
        self.assertEqual(TransportCalculation.objects.count(), 0)


class CalculationListViewTest(TestCase):
    def setUp(self):
        # Cria um veículo de teste
        self.vehicle = Vehicle.objects.create(
            name="Caminhão Teste", max_capacity=10000, cost_per_km=Decimal("5.00")
        )
        # Cria dois cálculos de transporte
        self.calculation1 = TransportCalculation.objects.create(
            vehicle=self.vehicle,
            weight=8000,
            distance=600,
            total_cost=Decimal("3000.00"),
        )
        self.calculation2 = TransportCalculation.objects.create(
            vehicle=self.vehicle,
            weight=5000,
            distance=400,
            total_cost=Decimal("2000.00"),
        )
        self.client = Client()

    def test_calculation_list_view_status_code(self):
        """
        Testa se a página de listagem de cálculos retorna status 200 (OK).
        """
        response = self.client.get(reverse("calculation_list"))
        self.assertEqual(response.status_code, 200)

    def test_calculation_list_view_template_used(self):
        """
        Testa se o template correto está sendo utilizado.
        """
        response = self.client.get(reverse("calculation_list"))
        self.assertTemplateUsed(response, "core/calculation_list.html")

    def test_calculation_list_view_content(self):
        """
        Verifica se os detalhes dos cálculos são exibidos na página.
        """
        response = self.client.get(reverse("calculation_list"))
        # Verifica se o nome do veículo aparece
        self.assertContains(response, self.vehicle.name)
        # Verifica se os dados do primeiro cálculo são exibidos
        self.assertContains(response, self.calculation1.weight)
        self.assertContains(response, self.calculation1.distance)
        self.assertContains(response, self.calculation1.total_cost)
        # Verifica se os dados do segundo cálculo são exibidos
        self.assertContains(response, self.calculation2.weight)
        self.assertContains(response, self.calculation2.distance)
        self.assertContains(response, self.calculation2.total_cost)
