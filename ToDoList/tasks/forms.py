from django import forms
from .models import Task
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
import datetime

class TarefaForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Verifica se o formulário está sendo inicializado com uma instância de objeto
        if self.instance and self.instance.data_vencimento:
            valor_data_db = self.instance.data_vencimento

            # Se o valor for uma string no formato 'd/m/y', converta para o formato correto.
            # Se for um objeto date, isso não fará nada (o que é bom).
            if isinstance(valor_data_db, str):
                try:
                    # Converte a string 'd/m/y' para um objeto de data do Python
                    data_convertida = datetime.datetime.strptime(valor_data_db, '%d/%m/%Y').date()
                    # Define o valor inicial do campo do formulário
                    # Isso garante que o formulário renderize a data corretamente
                    self.initial['data_vencimento'] = data_convertida
                except ValueError:
                    # Se a string não estiver no formato esperado, ignore para evitar um erro fatal.
                    print(f"Erro de formato de data no DB: '{valor_data_db}'")
    class Meta:
        model = Task
        fields = ['titulo', 'descricao', 'data_vencimento', 'categoria']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-input'}),
            'descricao': forms.Textarea(attrs={'class': 'form-input form-textarea', 'rows': 5}),
            'data_vencimento': forms.DateInput(attrs={'type': 'date', 'class': 'form-input'}),
            'categoria': forms.HiddenInput(),
        }

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

class AtualizarPerfilForm(forms.Form):
    username = forms.CharField(required=False, label="Usuário")
    email = forms.EmailField(required=False)
    nova_senha = forms.CharField(widget=forms.PasswordInput, required=False)
    confirmar_senha = forms.CharField(widget=forms.PasswordInput, required=False)

    def clean(self):
        cleaned_data = super().clean()
        nova_senha = cleaned_data.get("nova_senha")
        confirmar_senha = cleaned_data.get("confirmar_senha")

        if nova_senha or confirmar_senha:
            if nova_senha != confirmar_senha:
                raise forms.ValidationError("As senhas não coincidem.")
