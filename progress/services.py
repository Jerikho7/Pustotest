import csv
from django.utils.timezone import now
from game.models import LevelPrize
from .models import PlayerLevel, PlayerPrize, PlayerBoost


def award_prizes_for_completed_level(player_level: PlayerLevel):
    """
    Выдаёт игроку все призы за пройденный уровень.
    Idempotent: повторный вызов не создаёт дубликаты.
    """
    if not player_level.is_completed:
        return

    level_prizes = LevelPrize.objects.filter(level=player_level.level)

    for lp in level_prizes:
        PlayerPrize.objects.get_or_create(
            player=player_level.player,
            prize=lp.prize,
            level=player_level.level,
            defaults={"received_at": now()},
        )


def grant_boost_to_player(player, boost, source="manual", expires_at=None):
    """
    Выдаёт игроку буст вручную или за уровень.
    """
    return PlayerBoost.objects.create(
        player=player,
        boost=boost,
        source=source,
        expires_at=expires_at,
    )


def export_player_levels_to_csv(file_path: str):
    """
    Выгрузка данных по игрокам и уровням в CSV.
    CSV содержит: player_id, level_title, is_completed, prizes
    """
    from .models import PlayerLevel

    with open(file_path, mode="w", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["player_id", "level_title", "is_completed", "prizes"])

        player_levels = (
            PlayerLevel.objects.select_related("player", "level")
            .prefetch_related("player__prizes__prize")
            .iterator(chunk_size=1000)
        )

        for pl in player_levels:
            prizes = [pp.prize.title for pp in pl.player.prizes.all() if pp.level_id == pl.level_id]
            writer.writerow([pl.player.id, pl.level.title, pl.is_completed, "; ".join(prizes)])
