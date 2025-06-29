from django.urls import include, path, reverse_lazy
from django.contrib.auth import views as auth_view
from .views import Homepage
from . import views


# url - view - template
app_name = 'leaderboard'

urlpatterns = [
    path('tasks/', include('tasks.urls')),
    path('homepage/', Homepage.as_view(), name='homepage'),
    path('relatorio/', views.relatorio_view, name='relatorio'),
    path('calendario/', views.calendario_view, name='calendario'),
    path('get-day-tasks/', views.get_day_tasks, name='get_day_tasks'),
    path('criar-liga/', views.criar_liga, name='criar_liga'),
    path('criar-liga/ligas/', views.minhas_ligas, name='minhas_ligas'),
    path('criar-liga/ligas/<int:liga_id>/', views.detalhe_liga, name='detalhe_liga'),
    path('ligas/entrar/', views.ingressar_liga, name='ingressar_liga'),
]