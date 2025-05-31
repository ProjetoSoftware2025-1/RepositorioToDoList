from django.shortcuts import render, reverse, get_object_or_404, redirect
from django.views.generic import ListView, CreateView, FormView, UpdateView, RedirectView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Task
from .forms import TarefaForm, ConcluirTarefaForm
import logging
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







class CadastrarUsuario(RedirectView):
    template_name = 'login.html'

