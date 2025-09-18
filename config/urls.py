from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from player.views import LoginView
from game.views import BoostListCreateView, LevelListCreateView, PrizeListCreateView, LevelPrizeListCreateView
from progress.views import PlayerLevelViewSet, PlayerBoostViewSet, PlayerPrizeViewSet

router = DefaultRouter()

# Player
router.register(r"login", LoginView)

# Game
router.register(r"boosts", BoostListCreateView)
router.register(r"levels", LevelListCreateView)
router.register(r"prizes", PrizeListCreateView)
router.register(r"level-prizes", LevelPrizeListCreateView)

# Progress
router.register(r"player-levels", PlayerLevelViewSet)
router.register(r"player-boosts", PlayerBoostViewSet)
router.register(r"player-prizes", PlayerPrizeViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
]
