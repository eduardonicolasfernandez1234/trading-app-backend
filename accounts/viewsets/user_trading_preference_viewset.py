from rest_framework import viewsets

from accounts.models import UserTradingPreference
from accounts.serializers import UserTradingPreferenceSerializer


class UserTradingPreferenceViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar preferencias de trading del usuario.
    """
    queryset = UserTradingPreference.objects.all()
    serializer_class = UserTradingPreferenceSerializer
