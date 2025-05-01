from encodings.punycode import T
import os
from django.shortcuts import render, redirect
from django.conf import settings
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, FormView, DetailView
from django import forms
from django.views import View
from django.contrib import messages
from django.core.files import File
from tablib import Dataset

from .forms import DocumentUploadForm, DriverValidationForm
from .resources import VehicleResource
from .models import Vehicle, TransportCalculation, Driver
from .services import TransportCalculator

from core.utils.ocr import DocumentOCR


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


class DocumentUploadView(View):
    """
    1ª etapa: faz upload da imagem, executa OCR e redireciona para validação.
    """

    template_name = 'core/driver_upload.html'
    form_class = DocumentUploadForm
    document_ocr = DocumentOCR()

    def get(self, request):
        return render(request, self.template_name, {'form': self.form_class()})

    def post(self, request):
        form = self.form_class(request.POST, request.FILES)
        if not form.is_valid():
            return render(request, self.template_name, {'form': form})

        image = form.cleaned_data['document_image']
        # salva temporariamente
        temp_path = os.path.join(settings.MEDIA_ROOT, "drivers")
        os.makedirs(temp_path, exist_ok=True)

        temp_image_path = os.path.join(temp_path, image.name)

        with open(temp_image_path, 'wb') as f:
            for chunk in image.chunks():
                f.write(chunk)

        # extrai dados
        data = self.document_ocr.extract_data_document(temp_image_path)
        # extrai imagem
        image = self.document_ocr.extract_image(temp_image_path)
        # armazena dados e caminho na sessão
        request.session['driver_data'] = data
        request.session['driver_image_path'] = image

        return redirect('driver_validate')


class DriverValidateView(View):
    """
    2ª etapa: mostra formulário com dados extraídos, permite correção.
    """

    template_name = 'core/driver_validate.html'
    form_class = DriverValidationForm

    def get(self, request):
        data = request.session.get('driver_data', {})
        initial = {
            'name': data.get('name', ''),
            'cpf': data.get('cpf', ''),
            'phone': data.get('phone', ''),
        }
        # prepara form
        form = self.form_class(initial=initial)
        url_image = os.path.relpath(request.session.get('driver_image_path', ''), settings.MEDIA_ROOT)
        url_image = "/media/" + url_image
        print(url_image)
        context = {
            'form': form,
            'doc_image_url': url_image,
        }
        return render(
            request,
            self.template_name,
            context,
        )

    def post(self, request):
        form = self.form_class(request.POST)
        image_path = request.session.get('driver_image_path')
        if not form.is_valid():
            return render(request, self.template_name, {'form': form})

        # salva Driver definitivo
        driver = form.save(commit=False)

        # anexar a imagem de documento ao campo image
        with open(image_path, 'rb') as f:
            driver.image.save(os.path.basename(image_path), File(f), save=False)
        driver.valid = True
        driver.save()

        # limpa sessão
        request.session.pop('driver_data', None)
        request.session.pop('driver_image_path', None)

        messages.success(request, "Motorista cadastrado com sucesso!")
        return redirect('driver_success')


class DriverSuccessView(View):
    """
    Página de sucesso após cadastro.
    """

    template_name = 'core/driver_success.html'

    def get(self, request):
        return render(request, self.template_name)


class DriverListView(ListView):
    """
    Exibe uma lista de todos os condutores cadastrados.
    """

    model = Driver
    template_name = 'core/driver_list.html'  # template que será renderizado
    context_object_name = 'drivers'  # nome da variável no contexto
    paginate_by = 20  # opcional: paginação


class DriverDetailView(DetailView):
    """
    Exibe os dados completos de um motorista.
    """

    model = Driver
    template_name = 'core/driver_detail.html'  # Template a ser usado
    context_object_name = 'driver'
