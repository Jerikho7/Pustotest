from django.db import models


class Boost(models.Model):
    """
    Тип буста (бонуса).
    Например: удвоение или утроение очков.
    """

    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    multiplier = models.PositiveIntegerField(default=2)

    class Meta:
        verbose_name = "Буст"
        verbose_name_plural = "Бусты"

    def __str__(self):
        return f"{self.name} (x{self.multiplier})"


class Level(models.Model):
    """
    Уровень игры.
    """

    title = models.CharField(max_length=100)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"Level {self.order}: {self.title}"


class Prize(models.Model):
    """
    Приз, который можно получить за прохождение уровня.
    """

    title = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.title


class LevelPrize(models.Model):
    """
    Связка: какой приз выдаётся за прохождение конкретного уровня.
    """

    level = models.ForeignKey(Level, on_delete=models.CASCADE, related_name="prizes")
    prize = models.ForeignKey(Prize, on_delete=models.CASCADE)
    received = models.DateField(null=True, blank=True)

    class Meta:
        unique_together = ("level", "prize")

    def __str__(self):
        return f"{self.level} → {self.prize}"
