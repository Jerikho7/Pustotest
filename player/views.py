from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Player
from .serializers import PlayerSerializer, LoginSerializer


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data["username"]

        player, created = Player.objects.get_or_create(username=username)
        points_added = player.add_login_points()

        return Response(
            {
                "player": PlayerSerializer(player).data,
                "points_added": points_added,
                "first_login": created,
            },
            status=status.HTTP_200_OK,
        )
