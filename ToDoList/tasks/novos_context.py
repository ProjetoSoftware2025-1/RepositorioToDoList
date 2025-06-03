from .models import Task
from django.utils import timezone

def lista_tarefas_do_dia(request):
    today = timezone.now().date()
    lista_tarefas = Task.objects.all().filter(
        user=request.user,
        completo=False,
        data_vencimento__date=today
    )
    total_tarefas = lista_tarefas.count()
    return {"lista_tarefas_do_dia": lista_tarefas, "total_tarefas_do_dia": total_tarefas}

def lista_tarefas_afazer(request):
    now = timezone.now()
    lista_tarefas = Task.objects.all().filter(
        user=request.user,
        completo=False,
        data_vencimento__gte=now
    )
    total_tarefas = lista_tarefas.count()
    return {"lista_tarefas_afazer": lista_tarefas, "total_tarefas_afazer": total_tarefas}

def lista_tarefas_concluidas(request):
    lista_tarefas = Task.objects.all().filter(
        user=request.user,
        completo=True,
    )
    total_tarefas = lista_tarefas.count()
    return {"lista_tarefas_concluidas": lista_tarefas, "total_tarefas_concluidas": total_tarefas}

def lista_tarefas_atrasadas(request):
    now = timezone.now()
    lista_tarefas = Task.objects.all().filter(
        user=request.user,
        data_vencimento__lt=now
    ).order_by('data_vencimento')
    total_tarefas = lista_tarefas.count()
    return {"lista_tarefas_atrasadas": lista_tarefas, "total_tarefas_atrasadas": total_tarefas}

def total_tarefas(request):
    total_tarefas_pessoal = Task.objects.all().filter(user=request.user, categoria='PESSOAL')
    total_tarefas_estudo = Task.objects.all().filter(user=request.user, categoria='ESTUDOS')
    total_tarefas_trabalho = Task.objects.all().filter(user=request.user, categoria='TRABALHO')
    return {"total_tarefas_pessoal": total_tarefas_pessoal.count(), "total_tarefas_estudos": total_tarefas_estudo.count(), "total_tarefas_trabalho": total_tarefas_trabalho.count()}