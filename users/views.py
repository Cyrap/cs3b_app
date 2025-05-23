from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

class UserLoginAPIView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer

    def post(self, request):
        response = super().post(request)

        if response.status_code == status.HTTP_200_OK:
            username = request.data.get("username")

            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                return Response(
                    {"error": "Хэрэглэгч олдсонгүй"}, status=status.HTTP_400_BAD_REQUEST
                )

            user_response = {
                "id": user.id,
                "username": user.username,
                "role": "",
            }

            return Response(
                {
                    "access": response.data["access"],
                    "refresh": response.data["refresh"],
                    "user": user_response,
                    "message": "Нэвтрэлт амжилттай",
                },
                status=status.HTTP_200_OK,
            )
        return Response({"error": "Хүчингүй токен"}, status=status.HTTP_400_BAD_REQUEST)