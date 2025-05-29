from django import forms
from .models import Task

class TarefaForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['titulo', 'descricao']


