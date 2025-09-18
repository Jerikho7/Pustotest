from rest_framework import serializers
from .models import PlayerLevel, PlayerBoost, PlayerPrize


class PlayerLevelSerializer(serializers.ModelSerializer):
    level_title = serializers.CharField(source="level.title", read_only=True)

    class Meta:
        model = PlayerLevel
        fields = ["id", "level_title", "is_completed", "score", "completed"]


class PlayerBoostSerializer(serializers.ModelSerializer):
    boost_name = serializers.CharField(source="boost.name", read_only=True)
    multiplier = serializers.IntegerField(source="boost.multiplier", read_only=True)

    class Meta:
        model = PlayerBoost
        fields = ["id", "boost_name", "multiplier", "source", "granted_at", "expires_at"]


class PlayerPrizeSerializer(serializers.ModelSerializer):
    prize_title = serializers.CharField(source="prize.title", read_only=True)
    level_title = serializers.CharField(source="level.title", read_only=True)

    class Meta:
        model = PlayerPrize
        fields = ["id", "prize_title", "level_title", "received_at"]
