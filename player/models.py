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
    last_login_date = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name = "Игрок"
        verbose_name_plural = "Игроки"
        ordering = ["-points"]

    def __str__(self):
        return f"Игрок {self.id} - {self.username} - первый вход в игру: {self.first_login}."

    def add_login_points(self, amount: int = 10) -> int:
        """
        Начисляем очки за вход.

        - При первом входе фиксируем дату/время (first_login).
        - Обновляем last_login.
        - Очки даём только один раз в день.
        """
        now = timezone.now()
        today = now.date()

        if not self.first_login:
            self.first_login = now

        self.last_login = now

        if self.last_login_date == today:
            self.save(update_fields=["last_login"])
            return 0

        self.points += amount
        self.last_login_date = today
        self.save()
        return amount
