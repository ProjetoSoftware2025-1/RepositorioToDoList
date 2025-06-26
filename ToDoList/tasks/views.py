from django.shortcuts import render, reverse, get_object_or_404, redirect
from django.views.generic import TemplateView, ListView, CreateView, FormView, UpdateView, RedirectView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import Task
from .forms import TarefaForm, ConcluirTarefaForm, CadastrarUsuario
import logging
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.contrib import messages
import datetime
from datetime import date
from django.db.models import Q
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash
from .forms import AtualizarPerfilForm
from leaderboard.models import Competidor, Participacao


logger = logging.getLogger(__name__)

# Create your views here.

class ListarTarefa(LoginRequiredMixin, TemplateView):
    template_name = "listatarefas.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        hoje = date.today()
        start_of_week = hoje - datetime.timedelta(days=hoje.weekday())
        end_of_week = start_of_week + datetime.timedelta(days=6)

        # Todas as tarefas do usuário
        todas_tarefas = Task.objects.filter(user=user)

        # Listas fixas
        context['lista_tarefas_do_dia'] = todas_tarefas.filter(data_vencimento=hoje, completo=False)
        context['lista_tarefas_atrasadas'] = todas_tarefas.filter(data_vencimento__lt=hoje, completo=False)
        context['lista_tarefas_afazer'] = todas_tarefas.filter(completo=False)
        context['lista_tarefas_da_semana'] = todas_tarefas.filter(data_vencimento__range=[start_of_week, end_of_week], completo=False).order_by('data_vencimento')

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

class VisualizarTarefa (LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = "visualizartarefa.html"
    model = Task

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        task_id = self.kwargs.get('pk')
        task = get_object_or_404(Task, pk=task_id)
        context['task'] = task

    def test_func(self):
        """Garante que o usuário só pode ver suas próprias tarefas"""
        task_id = self.kwargs.get('pk')
        task = get_object_or_404(Task, pk=task_id)
        return task.user == self.request.user

class AtualizarTarefa(UpdateView):
    template_name = "atualizartarefa.html"
    form_class = TarefaForm
    model = Task

    def form_valid(self, form):
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('task:listatarefas')

class ExcluirTarefa(LoginRequiredMixin, DeleteView):
    template_name = "confirmarexclusao.html"
    model = Task

    def get_success_url(self):
        return reverse('task:listatarefas')

# class ConcluirTarefa(LoginRequiredMixin, UpdateView):
#     model = Task
#     form_class = ConcluirTarefaForm
#     template_name = "confirmarconclusao.html"
#     success_url = reverse_lazy("task:listatarefas")

#     def get_initial(self):
#         initial = super().get_initial()
#         initial['completo'] = True
#         return initial

class ConcluirTarefa(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = ConcluirTarefaForm
    template_name = "confirmarconclusao.html"
    success_url = reverse_lazy("task:listatarefas")

    def get_initial(self):
        initial = super().get_initial()
        initial['completo'] = True
        return initial

    def form_valid(self, form):
        # Marcar a tarefa como concluída
        response = super().form_valid(form)

        # Buscar o competidor correspondente ao usuário logado
        try:
            competidor = self.request.user.competidor
        except Competidor.DoesNotExist:
            competidor = None

        # Se for um competidor, incrementar pontuação em todas as ligas
        if competidor:
            participacoes = Participacao.objects.filter(competidor=competidor)
            for participacao in participacoes:
                participacao.pontuacao += 1
                participacao.save()

        return response

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


class AtualizarPerfil(LoginRequiredMixin, FormView):
    template_name = 'atualizarperfil.html'
    form_class = AtualizarPerfilForm
    success_url = reverse_lazy('leaderboard:dashboard')

    def get_initial(self):
        return {
            'username': self.request.user.username,
            'email': self.request.user.email,
        }

    def form_valid(self, form):
        user = self.request.user
        data = form.cleaned_data

        # Só atualiza os campos se foram preenchidos
        if data.get('username'):
            user.username = data['username']

        if data.get('email'):
            user.email = data['email']

        if data.get('nova_senha') and data.get('confirmar_senha'):
            if data['nova_senha'] == data['confirmar_senha']:
                user.set_password(data['nova_senha'])
            else:
                messages.error(self.request, 'As senhas não coincidem.')
                return self.form_invalid(form)

        user.save()
        messages.success(self.request, 'Seus dados foram atualizados com sucesso.')
        return redirect(self.success_url)

    def form_invalid(self, form):
        messages.error(self.request, 'Por favor, corrija os erros abaixo.')
        return super().form_invalid(form)
