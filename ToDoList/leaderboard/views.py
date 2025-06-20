from django.shortcuts import render
from django.views.generic import ListView
from tasks.models import Task

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

