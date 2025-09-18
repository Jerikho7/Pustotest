from django.urls import path
from .views import (
    BoostListCreateView,
    LevelListCreateView,
    PrizeListCreateView,
    LevelPrizeListCreateView,
)

urlpatterns = [
    path("boosts/", BoostListCreateView.as_view(), name="boost-list"),
    path("levels/", LevelListCreateView.as_view(), name="level-list"),
    path("prizes/", PrizeListCreateView.as_view(), name="prize-list"),
    path("level-prizes/", LevelPrizeListCreateView.as_view(), name="level-prize-list"),
]
