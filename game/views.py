from rest_framework import generics
from .models import Boost, Level, Prize, LevelPrize
from .serializers import (
    BoostSerializer,
    LevelSerializer,
    PrizeSerializer,
    LevelPrizeSerializer,
)


class BoostListCreateView(generics.ListCreateAPIView):
    queryset = Boost.objects.all()
    serializer_class = BoostSerializer


class LevelListCreateView(generics.ListCreateAPIView):
    queryset = Level.objects.all()
    serializer_class = LevelSerializer


class PrizeListCreateView(generics.ListCreateAPIView):
    queryset = Prize.objects.all()
    serializer_class = PrizeSerializer


class LevelPrizeListCreateView(generics.ListCreateAPIView):
    queryset = LevelPrize.objects.select_related("level", "prize")
    serializer_class = LevelPrizeSerializer
