from django.shortcuts import render, reverse
from django.views.generic import ListView, CreateView, FormView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Task
from .forms import TarefaForm

# Create your views here.

class CriarTarefa(LoginRequiredMixin, FormView):
    template_name = "criartarefa.html"
    form_class = TarefaForm

    def form_valid(self, form):
        tarefa = form.save(commit=False)
        tarefa.user = self.request.user
        tarefa.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('leaderboard:homepage')

class AtualizarTarefa(UpdateView):
    template_name = "atualizartarefa.html"
    form_class = TarefaForm
    model = Task

    def form_valid(self, form):
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('leaderboard:homepage')

