import uuid
from django.db import models
from django.contrib.auth.models import User
from users.models import UserProfile  # Importa o UserProfile de outro app


def gerar_codigo_convite() -> str:
    """
    Gera um código curto e único a partir de um UUID4.
    """
    return uuid.uuid4().hex[:8].upper()  # Ex: 'A1B2C3D4'


class Competidor(models.Model):
    """
    Extende o usuário com o papel de competidor.
    Nem todo usuário é competidor.
    """
    usuario = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="competidor",
    )

    def __str__(self):
        return f"{self.usuario.username}"


class Liga(models.Model):
    """
    Ligas em que competidores podem se associar.
    """
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)
    data_inicio = models.DateField(null=True, blank=True)
    data_fim = models.DateField(null=True, blank=True)
    codigo_convite = models.CharField(
        max_length=20,
        unique=True,
        default=gerar_codigo_convite,
        help_text="Código para ingresso na liga.",
    )

    competidores = models.ManyToManyField(
        Competidor,
        through="Participacao",
        related_name="ligas",
    )

    class Meta:
        verbose_name = "liga"
        verbose_name_plural = "ligas"

    def __str__(self):
        return self.nome


class Participacao(models.Model):
    """
    Representa a participação de um competidor em uma liga.
    """
    competidor = models.ForeignKey(
        Competidor,
        on_delete=models.CASCADE,
        related_name="participacoes",
    )
    liga = models.ForeignKey(
        Liga,
        on_delete=models.CASCADE,
        related_name="participacoes",
    )
    pontuacao = models.IntegerField(default=0)
    data_entrada = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("competidor", "liga")
        verbose_name = "participação"
        verbose_name_plural = "participações"

    def __str__(self):
        return f"{self.competidor} em {self.liga} — {self.pontuacao} pts"


class Ranking(models.Model):
    """
    Ranking de usuários (UserProfile) por liga.
    """
    perfil = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name="rankings"
    )
    liga = models.ForeignKey(
        Liga,
        on_delete=models.CASCADE,
        related_name="rankings"
    )
    posicao = models.PositiveIntegerField()
    ultima_atualizacao = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("perfil", "liga")
        ordering = ["posicao"]

    def __str__(self):
        return f"{self.perfil.user.username} - {self.liga.nome} ({self.posicao}º)"
