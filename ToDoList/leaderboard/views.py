import json
from datetime import datetime, date
import calendar
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView
from tasks.models import Task
from collections import defaultdict
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta, datetime
from django.contrib.auth.models import User
from django.http import HttpResponse
from .forms import LigaForm
from .models import Competidor, Participacao, Liga
from django.contrib import messages
from .forms import IngressoLigaForm
from tasks.models import Task

# Create your views here.
class Homepage(ListView):
    template_name = "dashboard.html"
    model = Task

@login_required
def relatorio_view(request):
    hoje = date.today()
    inicio_semana = hoje - timedelta(days=hoje.weekday())

    tarefas_usuario = Task.objects.filter(user=request.user)

    total_concluidas = tarefas_usuario.filter(completo=True).count()
    total_criadas = tarefas_usuario.count()

    percentual_conclusao = int((total_concluidas / total_criadas) * 100) if total_criadas > 0 else 0

    dados_relatorio = {
        "total_tasks": total_criadas,
        "tasks_concluidas": total_concluidas,
        "tasks_pendentes": tarefas_usuario.filter(completo=False).count(),
        "performance_semanal": [
            {
                "semana": "Esta Semana",
                "concluidas": tarefas_usuario.filter(completo=True, criado_em__date__gte=inicio_semana).count()
            },
            {
                "semana": "Hoje",
                "concluidas": tarefas_usuario.filter(completo=True, criado_em__date=hoje).count()
            }
        ]
    }

    # Se precisar da lista completa de tarefas para a tabela
    context = {
        "dados_relatorio": dados_relatorio,
        "percentual_conclusao": percentual_conclusao,
        "total_tarefas_trabalho": tarefas_usuario.filter(categoria__iexact='Trabalho').count(),
        "total_tarefas_estudos": tarefas_usuario.filter(categoria__iexact='Estudos').count(),
        "total_tarefas_pessoal": tarefas_usuario.filter(categoria__iexact='Pessoal').count(),
        "total_tarefas_atrasadas": tarefas_usuario.filter(completo=False, data_vencimento__lt=hoje).count(),
        "total_tarefas_afazer": tarefas_usuario.filter(completo=False, data_vencimento__gte=hoje).count(),
        "total_tarefas_concluidas": total_concluidas,
        "total_tarefas_concluidas_hoje": dados_relatorio["performance_semanal"][1]["concluidas"],
        "total_tarefas_concluidas_semana": dados_relatorio["performance_semanal"][0]["concluidas"],
        "lista_todas_tarefas": tarefas_usuario,  # Para popular a tabela
    }

    return render(request, 'relatorio.html', context)

@login_required
def calendario_view(request):
    today = timezone.now().date()
    
    # Obter o mês e ano atual ou dos parâmetros GET
    current_month = int(request.GET.get('month', today.month))
    current_year = int(request.GET.get('year', today.year))
    
    # Validar mês e ano
    if current_month < 1 or current_month > 12:
        current_month = today.month
    if current_year < 2020 or current_year > 2030:
        current_year = today.year
    
    # Criar data do primeiro dia do mês
    first_day = datetime(current_year, current_month, 1).date()
    
    # Calcular último dia do mês
    last_day = datetime(current_year, current_month, 
                       calendar.monthrange(current_year, current_month)[1]).date()
    
    # Calcular primeiro dia da semana do calendário (domingo anterior se necessário)
    calendar_start = first_day - timedelta(days=first_day.weekday() + 1)
    if first_day.weekday() == 6:  # Se o primeiro dia é domingo
        calendar_start = first_day
    
    # Calcular último dia da semana do calendário (sábado posterior se necessário)
    calendar_end = last_day + timedelta(days=(5 - last_day.weekday()))
    if last_day.weekday() == 5:  # Se o último dia é sábado
        calendar_end = last_day
    
    # Obter todas as tarefas do usuário no período do calendário
    user_tasks = Task.objects.filter(
        user=request.user,
        data_vencimento__range=[calendar_start, calendar_end]
    ).order_by('data_vencimento')
    
    # Organizar tarefas por data de criação
    tasks_by_date = {}
    for task in user_tasks:
        task_date = task.data_vencimento
        if task_date not in tasks_by_date:
            tasks_by_date[task_date] = []
        tasks_by_date[task_date].append(task)
    
    # Construir semanas do calendário
    calendar_weeks = []
    current_date = calendar_start
    
    while current_date <= calendar_end:
        week = []
        for day in range(7):  # 7 dias da semana
            day_tasks = tasks_by_date.get(current_date, [])
            
            # Limitar a 3 tarefas mostradas por dia
            visible_tasks = day_tasks[:3]
            extra_tasks = len(day_tasks) - 3 if len(day_tasks) > 3 else 0
            
            day_info = {
                'date': current_date,
                'day': current_date.day,
                'is_today': current_date == today,
                'other_month': current_date.month != current_month,
                'tasks': visible_tasks,
                'task_count': len(day_tasks),
                'extra_tasks': extra_tasks
            }
            
            week.append(day_info)
            current_date += timedelta(days=1)
        
        calendar_weeks.append(week)
        
        # Parar se já passou do final do mês e completou a semana
        if current_date > calendar_end:
            break
    
    # Estatísticas para o cabeçalho
    # Tarefas hoje
    tarefas_hoje = Task.objects.filter(
        user=request.user,
        data_vencimento=today
    ).count()
    
    # Tarefas desta semana
    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=6)
    
    tarefas_semana = Task.objects.filter(
        user=request.user,
        data_vencimento__range=[start_of_week, end_of_week]
    ).count()
    
    # Tarefas deste mês
    tarefas_mes = Task.objects.filter(
        user=request.user,
        data_vencimento__month=today.month,
        data_vencimento__year=today.year
    ).count()
    
    # Tarefas vencendo hoje
    tarefas_vencendo = Task.objects.filter(
        user=request.user,
        data_vencimento=today,
        completo=False
    ).count()
    
    # Pontuação do usuário (assumindo que existe um sistema de pontos)
    user_points = getattr(request.user, 'points', 0)
    
    # Nome do mês atual
    month_names = [
        'Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
        'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'
    ]
    current_month_name = month_names[current_month - 1]
    
    context = {
        'calendar_weeks': calendar_weeks,
        'current_month_name': current_month_name,
        'current_year': current_year,
        'current_month': current_month,
        'tarefas_hoje': tarefas_hoje,
        'tarefas_semana': tarefas_semana,
        'tarefas_mes': tarefas_mes,
        'tarefas_vencendo': tarefas_vencendo,
        'user_points': user_points,
        'today': today,
    }
    
    return render(request, 'calendario.html', context)


@login_required
def get_day_tasks(request):
    """
    View AJAX para obter tarefas de um dia específico
    """
    if request.method == 'GET':
        date_str = request.GET.get('date')
        if not date_str:
            return JsonResponse({'error': 'Data não fornecida'}, status=400)
        
        try:
            date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            return JsonResponse({'error': 'Formato de data inválido'}, status=400)
        
        # Obter tarefas do dia
        tasks = Task.objects.filter(
            user=request.user,
            data_vencimento=date_obj
        ).order_by('data_vencimento')
        
        # Formatar tarefas para JSON
        tasks_data = []
        for task in tasks:
            tasks_data.append({
                'id': task.id,
                'titulo': task.titulo,
                'descricao': task.descricao,
                'categoria': task.get_categoria_display(),
                'categoria_class': task.categoria.lower(),
                'completo': task.completo,
                'criado_em': task.criado_em.strftime('%H:%M'),
                'data_vencimento': task.data_vencimento.strftime('%d/%m/%Y') if task.data_vencimento else None,
            })

        return JsonResponse({
            'date': date_obj.strftime('%d/%m/%Y'),
            'tasks': tasks_data
        })

    
    return JsonResponse({'error': 'Método não permitido'}, status=405)

def criar_liga(request):
    if request.method == 'POST':
        form = LigaForm(request.POST)
        if form.is_valid():
            liga = form.save()

            # Garante que o usuário tenha um perfil Competidor
            competidor, created = Competidor.objects.get_or_create(usuario=request.user)

            # Cria a participação do criador na liga
            Participacao.objects.create(
                competidor=competidor,
                liga=liga,
                pontuacao=0  # opcional
            )

            return redirect('leaderboard:detalhe_liga', liga_id=liga.id)
    else:
        form = LigaForm()

    return render(request, 'criar_liga.html', {'form': form})

@login_required
def minhas_ligas(request):
    try:
        competidor = request.user.competidor
        ligas = competidor.ligas.all()  # relacionamento ManyToMany
    except Competidor.DoesNotExist:
        ligas = []

    return render(request, 'minhas_ligas.html', {'ligas': ligas})

@login_required
def detalhe_liga(request, liga_id):
    liga = get_object_or_404(Liga, id=liga_id)

    # Participações da liga ordenadas por pontuação decrescente
    participacoes = liga.participacoes.order_by('-pontuacao')

    return render(request, 'detalhe_liga.html', {
        'liga': liga,
        'participacoes': participacoes,
    })


@login_required
def ingressar_liga(request):
    if request.method == 'POST':
        form = IngressoLigaForm(request.POST)
        if form.is_valid():
            codigo = form.cleaned_data['codigo_convite'].strip().upper()

            # Tenta encontrar a liga pelo código
            liga = get_object_or_404(Liga, codigo_convite=codigo)

            # Garante que o usuário seja um competidor
            competidor, _ = Competidor.objects.get_or_create(usuario=request.user)

            # Verifica se já participa
            if Participacao.objects.filter(competidor=competidor, liga=liga).exists():
                messages.info(request, f"Você já participa da liga '{liga.nome}'.")
            else:
                Participacao.objects.create(competidor=competidor, liga=liga)
                messages.success(request, f"Você entrou na liga '{liga.nome}' com sucesso!")

            return redirect('leaderboard:detalhe_liga', liga_id=liga.id)
    else:
        form = IngressoLigaForm()

    return render(request, 'ingressar_liga.html', {'form': form})

def relatorio_view(request):
    hoje = date.today()
    inicio_semana = hoje - timedelta(days=hoje.weekday())

    tarefas_usuario = Task.objects.filter(user=request.user)
    tarefas_concluidas = tarefas_usuario.filter(completo=True)

    # Contagens de tarefas concluídas com base em data_conclusao
    total_tarefas_concluidas_hoje = tarefas_concluidas.filter(data_conclusao=hoje).count()
    total_tarefas_concluidas_semana = tarefas_concluidas.filter(data_conclusao__gte=inicio_semana).count()
    total_tarefas_concluidas = tarefas_concluidas.count()

    # Tarefas criadas (completo ou não)
    total_tarefas_criadas = tarefas_usuario.count()
    
    # Status: Em progresso e atrasadas
    total_tarefas_em_progresso = tarefas_usuario.filter(completo=False, data_vencimento__gte=hoje).count()
    total_tarefas_atrasadas = tarefas_usuario.filter(completo=False, data_vencimento__lt=hoje).count()

    # Por categoria
    total_tarefas_trabalho = tarefas_usuario.filter(categoria__iexact='Trabalho').count()
    total_tarefas_estudos = tarefas_usuario.filter(categoria__iexact='Estudos').count()
    total_tarefas_pessoal = tarefas_usuario.filter(categoria__iexact='Pessoal').count()

    # Percentual de conclusão
    percentual_conclusao = 0
    if total_tarefas_criadas > 0:
        percentual_conclusao = int((total_tarefas_concluidas / total_tarefas_criadas) * 100)

    # Atribuir status manual para cada tarefa
    lista_todas_tarefas = []
    for tarefa in tarefas_usuario:
        if tarefa.completo:
            tarefa.status = 'CONCLUIDA'
        elif tarefa.data_vencimento < hoje:
            tarefa.status = 'ATRASADA'
        else:
            tarefa.status = 'EM_PROGRESSO'
        lista_todas_tarefas.append(tarefa)

    context = {
        'total_tarefas_concluidas_hoje': total_tarefas_concluidas_hoje,
        'total_tarefas_concluidas_semana': total_tarefas_concluidas_semana,
        'total_tarefas_concluidas': total_tarefas_concluidas,
        'total_tarefas_afazer': total_tarefas_em_progresso,
        'total_tarefas_atrasadas': total_tarefas_atrasadas,
        'percentual_conclusao': percentual_conclusao,
        'total_tarefas_trabalho': total_tarefas_trabalho,
        'total_tarefas_estudos': total_tarefas_estudos,
        'total_tarefas_pessoal': total_tarefas_pessoal,
        'lista_todas_tarefas': lista_todas_tarefas,
    }

    return render(request, 'relatorio.html', context)