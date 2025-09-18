from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import PlayerLevel, PlayerBoost, PlayerPrize
from .serializers import (
    PlayerLevelSerializer,
    PlayerBoostSerializer,
    PlayerPrizeSerializer,
)


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

