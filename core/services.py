from decimal import Decimal
from .models import Vehicle


class TransportCalculator:
    """
    Classe de serviço responsável pelo cálculo do custo de transporte.
    Segue os princípios da Clean Architecture separando a lógica de negócio
    da camada de infraestrutura (models) e da camada de apresentação (views).
    """

    def __init__(self, distance_km: int = 600):
        self.distance_km = distance_km

    def get_vehicles(self):
        """
        Retorna todos os veículos disponíveis.
        """
        return Vehicle.objects.all()

    def calculate_cost(self, peso: int) -> Decimal:
        """
        Calcula o custo de transporte para um dado peso.

        A lógica de seleção de veículos ou combinação dos mesmos deve ser definida
        conforme as regras de negócio. Neste exemplo simples, vamos selecionar o
        veículo com capacidade suficiente e de menor custo.

        :param peso: Peso total da carga em kg.
        :return: Custo total do transporte para a distância definida.
        """
        # Buscar veículos com capacidade suficiente para o peso
        # Ordenar pelo menor custo_por_km para otimização
        veiculos_disponiveis = Vehicle.objects.filter(max_capacity__gte=peso).order_by(
            "cost_per_km"
        )

        if veiculos_disponiveis.exists():
            veiculo = veiculos_disponiveis.first()
            custo_total = veiculo.cost_per_km * self.distance_km
            return custo_total

        # Se nenhum veículo individual suportar a carga, implementar a lógica para combinação
        # Exemplo: distribuir a carga em vários veículos (lógica simplificada e a ser expandida)
        custo_total = 0
        carga_restante = peso
        # Ordenar todos os veículos por custo, independente da capacidade mínima
        veiculos = Vehicle.objects.all().order_by("cost_per_km")
        for veiculo in veiculos:
            if carga_restante <= 0:
                break
            # Quantos veículos desse tipo são necessários?
            num_veiculos = (
                carga_restante + veiculo.max_capacity - 1
            ) // veiculo.max_capacity
            custo_total += num_veiculos * veiculo.custo_por_km * self.distance_km
            carga_restante -= num_veiculos * veiculo.max_capacity

        return custo_total

    def calculate_cost_with_vehicle(
        self, vehicle: Vehicle, weight: int, distance: int
    ) -> Decimal:
        """
        Calcula o custo total de transporte para o veículo selecionado, com base na distância.
        Valida se o veículo escolhido suporta o peso informado.

        :param vehicle: Veículo selecionado.
        :param weight: Peso da carga em kg.
        :param distance: Distância a ser percorrida em km.
        :return: Custo total do transporte.
        :raises ValueError: Caso o peso exceda a capacidade do veículo.
        """
        if weight > vehicle.max_capacity:
            raise ValueError(
                "O peso informado excede a capacidade do veículo selecionado."
            )
        return vehicle.cost_per_km * distance
