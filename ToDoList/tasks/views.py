from django.shortcuts import render, reverse, get_object_or_404
from django.views.generic import ListView, CreateView, FormView, UpdateView, RedirectView
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

class ConcluirTarefa(LoginRequiredMixin, RedirectView):
    pattern_name = 'leaderboard:homepage'

    def get_object(self):
        return get_object_or_404(Task, pk=self.kwargs['pk'])

    def get(self, request, *args, **kwargs):
        tarefa = self.get_object()
        tarefa.concluido = True
        tarefa.save()
        return super().get(request, *args, **kwargs)


class DesmarcarTarefa(LoginRequiredMixin, RedirectView):
    pattern_name = 'leaderboard:homepage'

    def get_object(self):  # Obtém a tarefa a ser manipulada pelo PK da URL
        return get_object_or_404(Task, pk=self.kwargs['pk'])

    def get(self, request, *args, **kwargs): # Este método é chamado para requisições GET (cliques em links)
        tarefa = self.get_object()
        tarefa.concluido = False
        tarefa.save()
        return super().get(request, *args, **kwargs)




