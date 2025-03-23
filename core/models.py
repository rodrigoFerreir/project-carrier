from django.db import models


class Vehicle(models.Model):
    """
    Model que representa um veículo de transporte.
    Cada veículo possui:
      - nome: identificador do veículo;
      - capacidade_maxima: capacidade máxima de carga (em kg);
      - custo_por_km: custo para rodar por km.
    """

    name = models.CharField(max_length=100)
    max_capacity = models.PositiveIntegerField(help_text="Capacidade máxima em kg")
    cost_per_km = models.DecimalField(
        max_digits=10, decimal_places=2, help_text="Custo por km rodado"
    )

    def __str__(self):
        return self.name


class TransportCalculation(models.Model):
    """
    Registro de cálculos de transporte realizados pelo sistema.
    """

    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    weight = models.PositiveIntegerField(help_text="Peso da carga em kg")
    distance = models.PositiveIntegerField(help_text="Distância percorrida em km")
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)
    calculated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.vehicle.name} - {self.weight}kg - {self.distance}km - R$ {self.total_cost}"
