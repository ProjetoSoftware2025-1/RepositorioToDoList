from django.db import models
from django.contrib.auth.models import User  #usuário padrão do django

class Task(models.Model):
    titulo = models.CharField(max_length=255)
    descricao = models.TextField()
    completo = models.BooleanField(default=False)
    criado_em = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.titulo
