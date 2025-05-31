from django import forms
from .models import Task
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class TarefaForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['titulo', 'descricao']

class ConcluirTarefaForm(forms.ModelForm):
    class Meta:
        model = Task
        fields= ['completo']
        widgets = {
            'completo': forms.HiddenInput(),
        }


class CadastrarUsuario(UserCreationForm):
    nome = forms.CharField(max_length=150, required=True, label='Nome completo')

    class Meta:
        model = User
        fields = ['nome', 'username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['nome']
        if commit:
            user.save()
        return user