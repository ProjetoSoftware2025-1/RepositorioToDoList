from django.db import models
from django.contrib.auth.models import User  #reutilizando o user padrão do django

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  #cada usuário terá um perfil, abordagem recomendada na documentaçaõ do django
    # score_semanal = models.IntegerField(default=0)
    # score_total = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username
