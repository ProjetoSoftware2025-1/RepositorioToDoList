from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_view
from .views import CriarTarefa, AtualizarTarefa

# url - view - template
app_name = 'task'

urlpatterns = [
    path('criartarefa/', CriarTarefa.as_view(), name='criartarefa'),
    path('atualizartarefa/<int:pk>', AtualizarTarefa.as_view(), name='atualizartarefa')
]
