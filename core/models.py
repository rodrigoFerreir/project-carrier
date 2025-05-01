from django.db import models


class BaseModel(models.Model):
    """
    Classe base para todos os modelos do sistema.
    Cada modelo herda dessa classe para ter os campos padrão.
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Vehicle(BaseModel):
    """
    Model que representa um veículo de transporte.
    Cada veículo possui:
      - nome: identificador do veículo;
      - capacidade_maxima: capacidade máxima de carga (em kg);
      - custo_por_km: custo para rodar por km.
    """

    name = models.CharField(max_length=100)
    plate = models.CharField(max_length=10, unique=True)
    category = models.ForeignKey('VehicleCategory', on_delete=models.CASCADE)
    driver = models.ForeignKey('Driver', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name

    @property
    def max_capacity(self):
        """
        Retorna a capacidade máxima do veículo.
        """
        return self.category.max_capacity

    @property
    def cost_per_km(self):
        """
        Retorna o custo por km do veículo.
        """
        return self.category.cost_per_km


class VehicleCategory(BaseModel):
    """
    Model que representa uma categoria de veículo.
    Cada categoria possui:
      - nome: identificador da categoria;
      - descrição: descrição da categoria.
    """

    name = models.CharField(max_length=100)
    description = models.TextField()
    max_capacity = models.PositiveIntegerField(help_text="Capacidade máxima em kg")
    cost_per_km = models.DecimalField(max_digits=10, decimal_places=2, help_text="Custo por km rodado")

    def __str__(self):
        return self.name


class TransportCalculation(BaseModel):
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


class Driver(BaseModel):
    """
    Model que representa um motorista.
    Cada motorista possui:
      - nome: nome do motorista;
      - cpf: CPF do motorista (único);
      - telefone: telefone do motorista.
    """

    name = models.CharField(max_length=100)
    cpf = models.CharField(max_length=11, unique=True)
    phone = models.CharField(max_length=15)
    valid = models.BooleanField(default=False, help_text="Indica se os dados do motorista foram validados")
    image = models.ImageField(upload_to='drivers/', null=True, blank=True)

    def __str__(self):
        return self.name
