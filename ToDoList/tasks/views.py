from django.shortcuts import render, reverse, get_object_or_404, redirect
from django.views.generic import ListView, CreateView, FormView, UpdateView, RedirectView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Task
from .forms import TarefaForm, ConcluirTarefaForm, CadastrarUsuario
import logging
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.contrib import messages
from datetime import date
from django.db.models import Q
from django.views.generic import TemplateView


logger = logging.getLogger(__name__)

# Create your views here.

class ListarTarefa(LoginRequiredMixin, TemplateView):
    template_name = "listatarefas.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        hoje = date.today()

        # Todas as tarefas do usuário
        todas_tarefas = Task.objects.filter(user=user)

        # Listas fixas
        context['lista_tarefas_do_dia'] = todas_tarefas.filter(data_vencimento=hoje)
        context['lista_tarefas_atrasadas'] = todas_tarefas.filter(data_vencimento__lt=hoje, completo=False)
        context['lista_tarefas_afazer'] = todas_tarefas.filter(completo=False)

        # Totais por categoria
        context['total_tarefas_afazer'] = todas_tarefas.filter(completo=False).count()
        context['total_tarefas_concluidas'] = todas_tarefas.filter(completo=True).count()
        context['total_tarefas_atrasadas'] = todas_tarefas.filter(data_vencimento__lt=hoje, completo=False).count()
        context['total_tarefas_trabalho'] = todas_tarefas.filter(categoria='TRABALHO').count()
        context['total_tarefas_estudos'] = todas_tarefas.filter(categoria='ESTUDOS').count()
        context['total_tarefas_pessoal'] = todas_tarefas.filter(categoria='PESSOAL').count()

        # Agora: só processa o filtro SE houver parâmetros de filtro
        data = self.request.GET.get('data')
        status = self.request.GET.get('status')
        categoria = self.request.GET.get('categoria')

        if data or status or categoria:
            tarefas_filtradas = todas_tarefas

            if data:
                tarefas_filtradas = tarefas_filtradas.filter(data_vencimento=data)

            if status == 'pendente':
                tarefas_filtradas = tarefas_filtradas.filter(completo=False)
            elif status == 'concluida':
                tarefas_filtradas = tarefas_filtradas.filter(completo=True)
            elif status == 'atrasada':
                tarefas_filtradas = tarefas_filtradas.filter(data_vencimento__lt=hoje, completo=False)

            if categoria:
                tarefas_filtradas = tarefas_filtradas.filter(categoria=categoria)

            # Adiciona o resultado ao contexto
            context['resultado_filtro'] = tarefas_filtradas

        return context

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