from rest_framework import viewsets

from accounts.models import UserRiskProfile
from accounts.serializers import UserRiskProfileSerializer


class UserRiskProfileViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar perfiles de riesgo del usuario.
    """
    queryset = UserRiskProfile.objects.all()
    serializer_class = UserRiskProfileSerializer
