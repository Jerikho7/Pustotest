from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from player.models import Player
from .models import PlayerLevel, PlayerBoost, PlayerPrize
from .serializers import (
    PlayerLevelSerializer,
    PlayerBoostSerializer,
    PlayerPrizeSerializer,
)
from .services import export_player_levels_to_csv


class PlayerLevelViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Эндпоинт для просмотра прогресса игрока по уровням.
    """

    serializer_class = PlayerLevelSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return PlayerLevel.objects.filter(player=self.request.user).select_related("level")


class PlayerBoostViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Эндпоинт для просмотра активных бустов игрока.
    """

    serializer_class = PlayerBoostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return PlayerBoost.objects.filter(player=self.request.user).select_related("boost")


class PlayerPrizeViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Эндпоинт для просмотра призов игрока.
    """

    serializer_class = PlayerPrizeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return PlayerPrize.objects.filter(player=self.request.user).select_related("prize", "level")


class PlayerProgressViewSet(viewsets.ViewSet):
    """
    Дополнительный вьюсет для операций над прогрессом игрока.
    """

    @action(detail=True, methods=["get"])
    def export(self, request, pk=None):
        """
        Вернуть CSV с прогрессом игрока.
        """
        player = Player.objects.get(pk=pk)
        return export_player_levels_to_csv(player)
