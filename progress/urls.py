from django.urls import path
from .views import (
    PlayerLevelViewSet,
    PlayerBoostViewSet,
    PlayerPrizeViewSet,
    PlayerProgressViewSet,
)

urlpatterns = [
    path("player_boosts/", PlayerBoostViewSet.as_view(), name="player-boost"),
    path("player_levels/", PlayerLevelViewSet.as_view(), name="layer-level"),
    path("player_prizes/", PlayerPrizeViewSet.as_view(), name="layer-prize"),
    path("progress/", PlayerProgressViewSet.as_view(), name="player-progress"),
]
