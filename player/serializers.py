from rest_framework import serializers
from .models import Player


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ["id", "username", "points", "first_login", "last_login"]
        read_only_fields = ["id", "points", "first_login", "last_login"]


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
