from django.urls import include, path, reverse_lazy
from django.contrib.auth import views as auth_view
from .views import Homepage
from . import views


# url - view - template
app_name = 'leaderboard'

urlpatterns = [
    path('tasks/', include('tasks.urls')),
    path('homepage/', Homepage.as_view(), name='homepage'),
    path('ranking/', views.ranking_view, name='ranking'),
    path('relatorio/', views.relatorio_view, name='relatorio'),
    path('calendario/', views.calendario_view, name='calendario'),
    path('api/day-tasks/', views.get_day_tasks, name='get_day_tasks'),
]