from django.db import models
from django.utils.timezone import now
import csv


class Player(models.Model):
    player_id = models.CharField(max_length=100)


class Level(models.Model):
    title = models.CharField(max_length=100)
    order = models.IntegerField(default=0)


class Prize(models.Model):
    title = models.CharField()


class PlayerLevel(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    completed = models.DateField()
    is_completed = models.BooleanField(default=False)
    score = models.PositiveIntegerField(default=0)


class LevelPrize(models.Model):
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    prize = models.ForeignKey(Prize, on_delete=models.CASCADE)
    received = models.DateField()


class PlayerPrize(models.Model):
    """Призы, выданные игроку за уровни."""

    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="prizes")
    prize = models.ForeignKey(Prize, on_delete=models.CASCADE)
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    received_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Приз игрока"
        verbose_name_plural = "Призы игроков"
        unique_together = ("player", "prize", "level")  # предотвращаем дубликаты


def award_prizes_for_completed_level(player_level: PlayerLevel):
    """Выдаёт игроку все призы за пройденный уровень.

    Args:
        player_level (PlayerLevel): объект прохождения уровня игроком.

    Особенности:
        - Проверяем, что уровень завершён.
        - Используем get_or_create для уникальности.
        - Метод idempotent: повторный вызов не создаёт дубликаты.
    """
    if not player_level.is_completed:
        # Если уровень ещё не завершён, ничего не делаем
        return

    # Получаем все призы, связанные с уровнем
    level_prizes = LevelPrize.objects.filter(level=player_level.level)

    for lp in level_prizes:
        # Выдаём игроку, если ещё не выдано
        PlayerPrize.objects.get_or_create(
            player=player_level.player, prize=lp.prize, level=player_level.level, defaults={"received_at": now()}
        )


def export_player_levels_to_csv(file_path: str):
    """
    Выгрузка данных по игрокам и уровням в CSV.

    Args:
        file_path (str): путь к файлу CSV.

    CSV содержит:
        player_id, level_title, is_completed, prizes
    """

    # Открываем файл для записи
    with open(file_path, mode="w", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        # Заголовки
        writer.writerow(["player_id", "level_title", "is_completed", "prizes"])

        # Используем iterator() для экономии памяти
        player_levels_qs = PlayerLevel.objects.select_related("player", "level").iterator(chunk_size=1000)

        for pl in player_levels_qs:
            # Получаем все призы игрока за текущий уровень
            prizes_qs = PlayerPrize.objects.filter(player=pl.player, level=pl.level)
            prize_titles = "; ".join(p.prize.title for p in prizes_qs) if prizes_qs.exists() else ""
            # Записываем строку в CSV
            writer.writerow([pl.player.player_id, pl.level.title, pl.is_completed, prize_titles])
