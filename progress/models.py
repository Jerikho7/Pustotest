from django.db import models

from game.models import Level, Prize, Boost
from player.models import Player


class PlayerBoost(models.Model):
    """
    Связка игрока и выданного буста.
    """

    SOURCE_CHOICES = [
        ("manual", "Вручную"),
        ("level", "За уровень"),
    ]

    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="boosts")
    boost = models.ForeignKey(Boost, on_delete=models.CASCADE)
    granted_at = models.DateTimeField(auto_now_add=True)
    source = models.CharField(max_length=20, choices=SOURCE_CHOICES, default="manual")
    expires_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "Выданный буст"
        verbose_name_plural = "Выданные бусты"
        ordering = ["-granted_at"]

    def __str__(self):
        return f"{self.player.username} → {self.boost.name} ({self.source})"


class PlayerLevel(models.Model):
    """
    Уровень игрока: информация о прохождении.
    """

    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="levels")
    level = models.ForeignKey(Level, on_delete=models.CASCADE, related_name="player_levels")
    completed = models.DateField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)
    score = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "Уровень игрока"
        verbose_name_plural = "Уровни игроков"
        unique_together = ("player", "level")

    def __str__(self):
        return f"{self.player.username} → {self.level.title} ({'пройден' if self.is_completed else 'не пройден'})"


class PlayerPrize(models.Model):
    """
    Призы, выданные игроку за уровни.
    """

    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="prizes")
    prize = models.ForeignKey(Prize, on_delete=models.CASCADE)
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    received_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Приз игрока"
        verbose_name_plural = "Призы игроков"
        unique_together = ("player", "prize", "level")

    def __str__(self):
        return f"{self.player.username} получил {self.prize.title} за {self.level.title}"
