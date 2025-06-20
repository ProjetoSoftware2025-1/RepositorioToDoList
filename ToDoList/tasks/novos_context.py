from .models import Task
from django.utils import timezone
import datetime

def lista_tarefas_do_dia(request):
    today = timezone.now()
    lista_tarefas = Task.objects.all().filter(
        completo=False,
        data_vencimento=today
    )
    total_tarefas = lista_tarefas.count()
    return {"lista_tarefas_do_dia": lista_tarefas, "total_tarefas_do_dia": total_tarefas}

def lista_tarefas_afazer(request):
    now = timezone.now()
    lista_tarefas = Task.objects.all().filter(
        completo=False,
        data_vencimento__gte=now
    )
    total_tarefas = lista_tarefas.count()
    return {"lista_tarefas_afazer": lista_tarefas, "total_tarefas_afazer": total_tarefas}

def lista_tarefas_concluidas(request):
    lista_tarefas = Task.objects.all().filter(
        completo=True,
    )
    total_tarefas = lista_tarefas.count()
    return {"lista_tarefas_concluidas": lista_tarefas, "total_tarefas_concluidas": total_tarefas}

def lista_tarefas_atrasadas(request):
    now = timezone.now()
    lista_tarefas = Task.objects.all().filter(
        data_vencimento__lt=now,
        completo=False
    ).order_by('data_vencimento')
    total_tarefas = lista_tarefas.count()
    return {"lista_tarefas_atrasadas": lista_tarefas, "total_tarefas_atrasadas": total_tarefas}

def total_tarefas(request):
    total_tarefas_pessoal = Task.objects.all().filter(categoria='PESSOAL')
    total_tarefas_estudo = Task.objects.all().filter(categoria='ESTUDOS')
    total_tarefas_trabalho = Task.objects.all().filter(categoria='TRABALHO')
    return {"total_tarefas_pessoal": total_tarefas_pessoal.count(), "total_tarefas_estudos": total_tarefas_estudo.count(), "total_tarefas_trabalho": total_tarefas_trabalho.count()}

def lista_tarefas_da_semana(request):
    today = timezone.localtime(timezone.now()).date()
    start_of_week = today - datetime.timedelta(days=today.weekday())
    end_of_week = start_of_week + datetime.timedelta(days=6)

    lista_tarefas_semana = Task.objects.filter(
        data_vencimento__range=[start_of_week, end_of_week],
        completo=False
    ).order_by('data_vencimento') # Opcional: ordenar as tarefas por data de vencimento


    return {"lista_tarefas_semana": lista_tarefas_semana}