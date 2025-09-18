from django.db import models
from django.utils import timezone

class Player(models.Model):
    """
    Игрок системы.

        Attributes:
            username (имя пользователя).
            first_login (для аналитики).
            last_login (последний вход).
            points (количество очков).
        """

    username = models.CharField(max_length=100, unique=True, verbose_name="Имя игрока")
    points = models.IntegerField(default=0, verbose_name="Количество очков игрока")
    first_login = models.DateTimeField(null=True, blank=True, verbose_name="Дата первого входа игрока")
    last_login = models.DateTimeField(null=True, blank=True, verbose_name="Дата последнего входа игрока")

    class Meta:
        verbose_name = "Игрок"
        verbose_name_plural = "Игроки"
        ordering = ["-points"]

    def __str__(self):
        return f"Игрок {self.id} - {self.username} - первый вход в игру: {self.first_login}."

    def add_points(self, amount: int = 10):
        """Начисляем очки при входе"""
        self.points += amount
        now = timezone.now()
        if not self.first_login:
            self.first_login = now
        self.last_login = now
        self.save()
        return amount
