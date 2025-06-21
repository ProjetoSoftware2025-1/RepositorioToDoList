from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_view
from .views import AtualizarPerfil, Pomodoro, CriarTarefa, AtualizarTarefa, ConcluirTarefa, ExcluirTarefa, ListarTarefa, Login, CadastroUsuario, SairView

# url - view - template
app_name = 'task'

urlpatterns = [
    path('', Login.as_view(), name='login'),
    path('listatarefas/', ListarTarefa.as_view(), name='listatarefas'),
    path('criartarefa/', CriarTarefa.as_view(), name='criartarefa'),
    path('atualizartarefa/<int:pk>', AtualizarTarefa.as_view(), name='atualizartarefa'),
    path('concluirtarefa/<int:pk>', ConcluirTarefa.as_view(), name='concluirtarefa'),
    path('excluirtarefa/<int:pk>', ExcluirTarefa.as_view(), name='excluirtarefa'),
    path('cadastro/', CadastroUsuario.as_view(), name='cadastro'),
    path('logout/', SairView.as_view(next_page='task:login'), name='logout'),
    path('pomodoro/', Pomodoro.as_view(), name='pomodoro'),
    path('editarperfil/', AtualizarPerfil.as_view(), name='editarperfil'),
    
    # path('password-reset/', auth_view.PasswordResetView.as_view(template_name='registration/password_reset.html'), name='password_reset'),
]
