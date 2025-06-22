import json
import datetime
import calendar
from django.shortcuts import render
from django.views.generic import ListView
from tasks.models import Task
from collections import defaultdict
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta, datetime
from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
class Homepage(ListView):
    template_name = "dashboard.html"
    model = Task

#dados mockados pra view de ranking
def ranking_view(request):
    usuarios_mock = [
        {"nome": "Alice", "score_semanal": 120, "score_total": 780},
        {"nome": "Bruno", "score_semanal": 110, "score_total": 750},
        {"nome": "Carla", "score_semanal": 150, "score_total": 800},
        {"nome": "Daniel", "score_semanal": 90, "score_total": 600},
        {"nome": "Eduarda", "score_semanal": 100, "score_total": 700},
        {"nome": "Fernando", "score_semanal": 130, "score_total": 790},
    ]

    # Ordenar por score_total
    usuarios_ordenados = sorted(usuarios_mock, key=lambda x: x["score_total"], reverse=True)

    ranking_users = []
    for i, usuario in enumerate(usuarios_ordenados, start=1):
        nome = usuario["nome"]
        user_data = {
            "username": nome,
            "first_name": nome,
            "get_full_name": f"{nome} da Silva"  # ou apenas nome se quiser
        }
        ranking_users.append({
            "user": user_data,
            "points": usuario["score_total"],
            "position": i
        })

    context = {
       "ranking_users": ranking_users,
       #"user": "Carla"  # Nome do usuário logado, para marcação (current-user)
    }

    return render(request, 'ranking.html', context)

def relatorio_view(request):
    # Dados mockados para o relatório
    dados_relatorio = {
        "total_tasks": 15,
        "tasks_concluidas": 12,
        "tasks_pendentes": 3,
        "performance_semanal": [
            {"semana": "Semana 1", "concluidas": 5},
            {"semana": "Semana 2", "concluidas": 7},
            {"semana": "Semana 3", "concluidas": 3},
            {"semana": "Semana 4", "concluidas": 8},
        ]
    }
    
    context = {
        "dados_relatorio": dados_relatorio,
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