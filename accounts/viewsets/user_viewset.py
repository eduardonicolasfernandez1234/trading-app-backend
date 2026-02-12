from rest_framework import viewsets

from accounts.models import User
from accounts.serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar usuarios del sistema.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
