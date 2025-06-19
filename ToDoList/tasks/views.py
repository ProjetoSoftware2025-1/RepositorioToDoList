from django.shortcuts import render, reverse, get_object_or_404, redirect
from django.views.generic import TemplateView, ListView, CreateView, FormView, UpdateView, RedirectView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Task
from .forms import TarefaForm, ConcluirTarefaForm, CadastrarUsuario
import logging
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.contrib import messages


logger = logging.getLogger(__name__)

# Create your views here.

class ListarTarefa(ListView):
    template_name = "listatarefas.html"
    model = Task

class CriarTarefa(LoginRequiredMixin, FormView):
    template_name = "criartarefa.html"
    form_class = TarefaForm

    def form_valid(self, form):
        tarefa = form.save(commit=False)
        tarefa.user = self.request.user
        tarefa.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('task:listatarefas')

class AtualizarTarefa(UpdateView):
    template_name = "atualizartarefa.html"
    form_class = TarefaForm
    model = Task

    def form_valid(self, form):
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('task:listatarefas')

class ExcluirTarefa(DeleteView):
    template_name = "listatarefas.html"
    model = Task

    def get_success_url(self):
        return reverse('task:listatarefas')

class ConcluirTarefa(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = ConcluirTarefaForm
    template_name = "confirmarconclusao.html"
    success_url = reverse_lazy("task:listatarefas")

    def get_initial(self):
        initial = super().get_initial()
        initial['completo'] = True
        return initial

class Login(LoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('leaderboard:homepage')
    
    def form_valid(self, form):
        messages.success(self.request, f'Bem-vindo, {form.get_user().username}!')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Credenciais inválidas. Tente novamente.')
        return super().form_invalid(form)

class CadastroUsuario(FormView):
    template_name = 'cadastro.html'
    form_class = CadastrarUsuario
    success_url = reverse_lazy('task:login')  # ou outro caminho de redirecionamento após cadastro

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Cadastro realizado com sucesso! Faça login para continuar.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Por favor, corrija os erros abaixo.')
        return super().form_invalid(form)

class SairView(LogoutView):
    next_page = 'task:login'

    def dispatch(self, request, *args, **kwargs):
        messages.success(request, "Você saiu com sucesso!")
        return super().dispatch(request, *args, **kwargs)
    
class Pomodoro(TemplateView):
    template_name= 'pomodoro.html'