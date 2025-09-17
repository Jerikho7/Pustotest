from django.db import models


class Player(models.Model):
    """
    Игрок системы.

    Attributes:
        username (уникальное имя игрока)
        joined_at (дата первого входа — для аналитики)
        last_login_at (последний вход)
        total_points (накопленные очки за ежедневные входы)
    """

    username = models.CharField(max_length=50, unique=True)
    joined_at = models.DateTimeField(auto_now_add=True)
    last_login_at = models.DateTimeField(null=True, blank=True)
    total_points = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "Игрок"
        verbose_name_plural = "Игроки"
        ordering = ["-total_points"]

    def __str__(self):
        return f"{self.username} ({self.total_points} очков)"

    def add_points(self, amount: int) -> None:
        """Начислить игроку очки."""
        self.total_points += amount
        self.save(update_fields=["total_points"])

    def give_boost(self, boost: "Boost", source: str = "manual"):
        """Выдать игроку буст."""
        return PlayerBoost.objects.create(player=self, boost=boost, source=source)


class Boost(models.Model):
    """
    Тип буста (бонуса).

    Attributes:
        name (название)
        description (описание)
        multiplier (множитель очков, например х2 или х3)
    """

    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    multiplier = models.PositiveIntegerField(default=2)

    class Meta:
        verbose_name = "Буст"
        verbose_name_plural = "Бусты"

    def __str__(self):
        return f"{self.name} (x{self.multiplier})"


class PlayerBoost(models.Model):
    """
    Связка игрока и выданного буста.

    Attributes:
        player (кому выдано)
        boost (какой буст)
        granted_at (дата выдачи)
        source (откуда пришёл — вручную/за уровень)
        expires_at (необязательно, дата окончания действия)
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
