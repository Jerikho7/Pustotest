from rest_framework import serializers
from .models import Boost, Level, Prize, LevelPrize


class BoostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Boost
        fields = ["id", "name", "description", "multiplier"]


class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level
        fields = ["id", "title", "order"]


class PrizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prize
        fields = ["id", "title"]


class LevelPrizeSerializer(serializers.ModelSerializer):
    level = LevelSerializer(read_only=True)
    prize = PrizeSerializer(read_only=True)

    class Meta:
        model = LevelPrize
        fields = ["id", "level", "prize", "received"]
