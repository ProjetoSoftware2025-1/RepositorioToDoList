from django.db import models
from django.contrib.auth.models import User  #usuário padrão do django
from django.utils import timezone

LISTA_CATEGORIAS = (
    ("PESSOAL", "Pessoal"),
    ("TRABALHO", "Trabalho"),
    ("ESTUDOS", "Estudos")
)
class Task(models.Model):
    titulo = models.CharField(max_length=255)
    descricao = models.TextField()
    categoria = models.CharField(max_length=15, choices=LISTA_CATEGORIAS)
    completo = models.BooleanField(default=False)
    criado_em = models.DateTimeField(auto_now_add=True)
    data_vencimento = models.DateField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.titulo
