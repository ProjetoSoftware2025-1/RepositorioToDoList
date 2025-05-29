from .models import Task

def lista_tarefas_afazer(request):
    lista_tarefas = Task.objects.all().filter(completo=False)
    return {"lista_tarefas_afazer": lista_tarefas}

def lista_tarefas_concluidas(request):
    lista_tarefas = Task.objects.all().filter(completo=True)
    return {"lista_tarefas_concluidas": lista_tarefas}