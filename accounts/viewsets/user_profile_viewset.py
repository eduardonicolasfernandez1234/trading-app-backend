from rest_framework import viewsets

from accounts.models import UserProfile
from accounts.serializers import UserProfileSerializer


class UserProfileViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar perfiles de usuario.
    """
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
