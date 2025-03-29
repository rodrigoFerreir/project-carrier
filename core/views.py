from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, FormView
from django import forms
from django.contrib import messages
from tablib import Dataset


from .resources import VehicleResource

from .models import Vehicle, TransportCalculation
from .services import TransportCalculator


# Formulário para importação de veiculos.
class UploadFileForm(forms.Form):
    file = forms.FileField()


# Formulário para receber o peso da carga.
class CostCalculationForm(forms.Form):
    weight = forms.IntegerField(
        label="Peso da Carga (kg)",
        min_value=100,
        help_text="Informe o peso da carga para calcular o custo do transporte.",
    )
    distance = forms.IntegerField(
        label="Distância (km)",
        min_value=1,
        help_text="Informe a distância a ser percorrida.",
    )
    vehicle = forms.ModelChoiceField(
        queryset=Vehicle.objects.all(),
        label="Veículo",
        help_text="Selecione o veículo para o transporte.",
    )


# View para exibir a lista de veículos disponíveis.
class VehicleListView(LoginRequiredMixin, ListView):

    model = Vehicle
    template_name = "core/vehicle_list.html"  # Crie este template para listar os veículos.
    context_object_name = "vehicles"

    # Opcional: você pode adicionar filtros ou ordenações na query.
    def get_queryset(self):
        return Vehicle.objects.all().order_by("name")


# View para realizar o cálculo do custo de transporte.
class CostCalculationView(LoginRequiredMixin, FormView):
    template_name = "core/calculate_cost.html"  # Crie este template para o formulário e o resultado.
    form_class = CostCalculationForm
    success_url = reverse_lazy("calculate_cost")

    def form_valid(self, form):
        # Obtém o peso informado no formulário
        weight = form.cleaned_data["weight"]
        distance = form.cleaned_data["distance"]
        vehicle = form.cleaned_data["vehicle"]

        calculator = TransportCalculator()
        try:
            cost = calculator.calculate_cost_with_vehicle(vehicle, weight, distance)
        except ValueError as e:
            form.add_error("weight", str(e))
            return self.form_invalid(form)

        TransportCalculation.objects.create(vehicle=vehicle, weight=weight, distance=distance, total_cost=cost)

        return self.render_to_response(
            self.get_context_data(form=form, cost=cost, weight=weight, distance=distance, vehicle=vehicle)
        )


class CalculationListView(LoginRequiredMixin, ListView):
    """
    View que lista todos os cálculos de transporte realizados.
    Os cálculos serão ordenados pela data de cálculo (do mais recente para o mais antigo).
    """

    model = TransportCalculation
    template_name = "core/calculation_list.html"
    context_object_name = "calculations"
    ordering = ["-calculated_at"]


class ImportVehiclesView(LoginRequiredMixin, FormView):
    template_name = "core/import_vehicles.html"
    form_class = UploadFileForm
    success_url = reverse_lazy("import_vehicles")

    def form_valid(self, form):
        file = form.cleaned_data["file"]
        dataset = Dataset()
        imported_data = dataset.load(
            file.read().decode("utf-8"), format=file.name.split(".")[-1]
        )  # Ajuste o formato conforme necessário
        vehicle_resource = VehicleResource()
        result = vehicle_resource.import_data(imported_data, dry_run=True)  # Teste de importação

        if not result.has_errors():
            vehicle_resource.import_data(imported_data, dry_run=False)  # Importação real
            messages.success(self.request, "Veículos importados com sucesso!")
        else:
            messages.error(self.request, "Erros encontrados durante a importação.")

        return super().form_valid(form)
