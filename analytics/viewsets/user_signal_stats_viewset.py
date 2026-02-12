from rest_framework import viewsets

from analytics.models import UserSignalStats
from analytics.serializers import UserSignalStatsSerializer


class UserSignalStatsViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar estadísticas agregadas de señales
    por usuario.
    """
    queryset = UserSignalStats.objects.all()
    serializer_class = UserSignalStatsSerializer
