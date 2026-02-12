from rest_framework_simplejwt.views import TokenObtainPairView

from accounts.serializers.jwt_serializer import EmailTokenObtainPairSerializer


class EmailTokenObtainPairView(TokenObtainPairView):
    serializer_class = EmailTokenObtainPairSerializer
