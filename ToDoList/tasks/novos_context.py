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
    return {"lista_tarefas_do_dia_geral": lista_tarefas, "total_tarefas_do_dia_geral": total_tarefas}

def lista_tarefas_afazer(request):
    now = timezone.now()
    lista_tarefas = Task.objects.all().filter(
        completo=False,
        data_vencimento__gte=now
    )
    total_tarefas = lista_tarefas.count()
    return {"lista_tarefas_afazer_geral": lista_tarefas, "total_tarefas_afazer_geral": total_tarefas}

def lista_tarefas_concluidas(request):
    lista_tarefas = Task.objects.all().filter(
        completo=True,
    )
    total_tarefas = lista_tarefas.count()
    return {"lista_tarefas_concluidas_geral": lista_tarefas, "total_tarefas_concluidas_geral": total_tarefas}

def lista_tarefas_atrasadas(request):
    now = timezone.now()
    lista_tarefas = Task.objects.all().filter(
        data_vencimento__lt=now,
        completo=False
    ).order_by('data_vencimento')
    total_tarefas = lista_tarefas.count()
    return {"lista_tarefas_atrasadas_geral": lista_tarefas, "total_tarefas_atrasadas_geral": total_tarefas}

def total_tarefas(request):
    total_tarefas_pessoal = Task.objects.all().filter(categoria='PESSOAL')
    total_tarefas_estudo = Task.objects.all().filter(categoria='ESTUDOS')
    total_tarefas_trabalho = Task.objects.all().filter(categoria='TRABALHO')
    return {"total_tarefas_pessoal_geral": total_tarefas_pessoal.count(), "total_tarefas_estudos_geral": total_tarefas_estudo.count(), "total_tarefas_trabalho_geral": total_tarefas_trabalho.count()}

