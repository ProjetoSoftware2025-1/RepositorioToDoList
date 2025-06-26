from django import forms
from .models import Liga

class LigaForm(forms.ModelForm):
    class Meta:
        model = Liga
        fields = ['nome', 'descricao', 'data_inicio', 'data_fim']
        widgets = {
            'data_inicio': forms.DateInput(attrs={'type': 'date'}),
            'data_fim': forms.DateInput(attrs={'type': 'date'}),
        }

class IngressoLigaForm(forms.Form):
    codigo_convite = forms.CharField(label="Código de Convite", max_length=20)