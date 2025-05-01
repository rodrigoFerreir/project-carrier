from django import forms
from .models import Driver


class DocumentUploadForm(forms.Form):
    """
    Form para upload de imagem do documento do motorista.
    """

    document_image = forms.ImageField(label="Foto do Documento")


class DriverValidationForm(forms.ModelForm):
    """
    Form para revisão e confirmação dos dados extraídos por OCR.
    """

    class Meta:
        model = Driver
        fields = ['name', 'cpf', 'phone', 'image', 'valid']
        widgets = {
            'valid': forms.HiddenInput(),  # Será setado manualmente
        }
