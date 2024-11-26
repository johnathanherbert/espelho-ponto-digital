from django import forms
from .models import EspelhoPonto

class UploadPDFForm(forms.ModelForm):
    class Meta:
        model = EspelhoPonto
        fields = ['arquivo']